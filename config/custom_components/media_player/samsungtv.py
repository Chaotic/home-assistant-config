"""
Support for interface with an Samsung TV.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/media_player.samsungtv/
"""
import asyncio
from datetime import timedelta
import logging
import threading
import os
import uuid

import voluptuous as vol

from homeassistant.components.media_player import (
    MEDIA_TYPE_CHANNEL, PLATFORM_SCHEMA, SUPPORT_NEXT_TRACK, SUPPORT_PAUSE,
    SUPPORT_PLAY, SUPPORT_PLAY_MEDIA, SUPPORT_PREVIOUS_TRACK, SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON, SUPPORT_VOLUME_MUTE, SUPPORT_VOLUME_STEP,
    SUPPORT_VOLUME_SET, SUPPORT_SELECT_SOURCE, MediaPlayerDevice)
from homeassistant.const import (
    CONF_NAME,
    STATE_OFF,
    STATE_ON
)
import homeassistant.helpers.config_validation as cv
from homeassistant.util import dt as dt_util


REQUIREMENTS = [
     'https://github.com/kdschlosser/'
     'samsungctl/archive/develop.zip#samsungctl==0.8.64b'
]

SAMSUNG_CONFIG_PATH = 'samsung_tv'

ICON_TV = 'mdi:television'
ICON_TV_OFF = 'mdi:television-off'
ICON_COMPONENT = 'mdi:video-input-component'
ICON_HDMI = 'mdi:video-input-hdmi'
ICON_SVIDEO = 'mdi:video-input-svideo'
ICON_USB = 'mdi:usb'
ICON_PC = 'mdi:console'
ICON_DLNA = 'mdi:dlna'
ICON_AV = 'mdi:audio-video'
ICON_YOUTUBE = 'mdi:youtube'
ICON_HULU = 'mdi:hulu'
ICON_NETFLIX = 'mdi:netflix'
ICON_PLEX = 'mdi:plex'
ICON_SPOTIFY = 'mdi:spotify'
ICON_AMAZON = 'mdi:amazon'
ICON_PLAYSTATION = 'mdi:playstation'
ICON_UNKNOWN = 'mdi:help'

_LOGGER = logging.getLogger(__name__)

CONF_DESCRIPTION = 'description'
CONF_ADD = 'add_tv'

KEY_PRESS_TIMEOUT = 1.2
KNOWN_DEVICES_KEY = 'samsungtv_known_devices'

SUPPORT_SAMSUNGTV = (
    SUPPORT_PAUSE |
    SUPPORT_VOLUME_STEP |
    SUPPORT_VOLUME_MUTE |
    SUPPORT_PREVIOUS_TRACK |
    SUPPORT_NEXT_TRACK |
    SUPPORT_TURN_OFF |
    SUPPORT_PLAY |
    SUPPORT_PLAY_MEDIA |
    SUPPORT_VOLUME_SET |
    SUPPORT_SELECT_SOURCE
)


SAMSUNG_TV_SCHEMA = vol.Schema({
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_DESCRIPTION): cv.string,
    vol.Optional(CONF_ADD): cv.boolean,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({})

_CONFIGURING = {}


def setup_platform(hass, config, add_entities, _=None):
    """Set up the Samsung TV platform."""

    config_path = hass.config.path(SAMSUNG_CONFIG_PATH)

    if not os.path.exists(config_path):
        os.mkdir(config_path)

    known_devices = hass.data.get(KNOWN_DEVICES_KEY, set())
    hass.data[KNOWN_DEVICES_KEY] = known_devices

    import samsungctl
    from samsungctl.upnp.discover import auto_discover

    config_files = list(
        os.path.join(config_path, file) for file in os.listdir(config_path)
            if file.endswith('config')
    )

    def callback(found_config):
        if found_config.uuid in known_devices:
            return

        _LOGGER.debug(str(found_config))
        known_devices.add(found_config.uuid)

        no_include = os.path.join(
            config_path,
            found_config.uuid + '.noinclude'
        )

        if os.path.exists(no_include):
            return

        if found_config.uuid not in _CONFIGURING:
            add_device(found_config, hass, config_path, add_entities)

    auto_discover.register_callback(callback)
    entities = []
    configs = []

    for config_file in config_files:
        _LOGGER.debug(config_file)
        samsung_config = samsungctl.Config.load(config_file)
        known_devices.add(samsung_config.uuid)
        configs += [samsung_config]

    auto_discover.start()

    for samsung_config in configs:
        entities += [SamsungTVDevice(samsung_config)]
    add_entities(entities)


def add_device(samsung_config, hass, config_path, add_entities):
    model = samsung_config.model
    uuid = samsung_config.uuid

    event = threading.Event()

    def samsung_configuration_callback(data):
        """Handle the entry of user PIN."""
        display_name = data.get('display_name')
        description = data.get('description')
        mac = data.get('mac')

        if display_name is None:
            display_name = samsung_config.display_name
        if description is None:
            description = samsung_config.description
        if mac is None:
            mac = samsung_config.mac

        samsung_config.display_name = display_name
        samsung_config.description = description
        samsung_config.mac = mac

        samsung_config.path = os.path.join(
            config_path,
            samsung_config.uuid + '.config'
        )

        hass.components.configurator.request_done(_CONFIGURING.pop(uuid))

        if samsung_config.method == 'encrypted':
            request_configuration(samsung_config, hass, add_entities)
        else:
            add_entities([SamsungTVDevice(samsung_config)])

        event.set()

    def do():
        event.wait(600.0)
        if not event.isSet():
            path = os.path.join(
                config_path,
                samsung_config.uuid + '.noinclude'
            )

            with open(path, 'w') as f:
                f.write('')

            hass.components.configurator.request_done(_CONFIGURING.pop(uuid))

    t = threading.Thread(target=do)
    t.daemon = True
    t.start()

    _CONFIGURING[uuid] = hass.components.configurator.request_config(
        model,
        samsung_configuration_callback,
        description='New TV discovered, would you like to add the TV?',
        description_image="/static/images/smart-tv.png",
        submit_caption="Accept",
        fields=[
            dict(
                id='display_name',
                name='Name: ' + samsung_config.display_name,
                type=''
            ),
            dict(
                id='description',
                name='Description: ' + samsung_config.description,
                type=''
            ),
            dict(
                id='mac',
                name='MAC Address : ' + str(samsung_config.mac),
                type=''
            )
        ]
    )


def request_configuration(samsung_config, hass, add_entities):
    """Request configuration steps from the user."""

    configurator = hass.components.configurator

    import samsungctl

    pin = []
    count = 0
    event = threading.Event()

    def samsung_configuration_callback(data):
        """Handle the entry of user PIN."""
        pin.append(data.get('pin'))
        event.set()

    def get_pin():
        global count

        if samsung_config.uuid in _CONFIGURING:
            count += 1
            event.clear()
            del pin[:]

            configurator.notify_errors(
                _CONFIGURING[samsung_config.uuid],
                "Failed to register, please try again."
            )
        else:
            _CONFIGURING[samsung_config.uuid] = configurator.request_config(
                samsung_config.display_name,
                samsung_configuration_callback,
                description='Enter the Pin shown on your Samsung TV.',
                description_image="/static/images/smart-tv.png",
                submit_caption="Confirm",
                fields=[{'id': 'pin', 'name': 'Enter the pin', 'type': ''}]
            )

        event.wait(60.0)

        if count == 3:
            _LOGGER.error(
                samsung_config.display_name + " TV: Pin entry failed"
            )
            return False
        elif not event.isSet():
            return None

        return pin[0]

    samsung_config.get_pin = get_pin

    def do():
        global count

        try:
            _ = samsungctl.Remote(samsung_config)
            add_entities([SamsungTVDevice(samsung_config)])
        except:
            pass

        hass.components.configurator.request_done(_CONFIGURING.pop(uuid))

    t = threading.Thread(target=do)
    t.daemon = True
    t.start()


class SamsungTVDevice(MediaPlayerDevice):
    """Representation of a Samsung TV."""

    def __init__(self, config):
        """Initialize the Samsung device."""
        from samsungctl import exceptions
        from samsungctl import Remote

        # Save a reference to the imported classes
        self._exceptions_class = exceptions
        self._remote_class = Remote
        self._config = config
        self._mac = self._config.mac
        self._uuid = self._config.uuid
        self._playing = True
        self._state = None
        self._remote = None
        self._key_source = False
        self._mute = False
        self._sources = []
        self._source = ''
        self._volume = 0.0
        self._entity_image = None
        self._tv_image = None

        if self._config.method == 'websocket':
            self._has_apps = True
        else:
            self._has_apps = False
        self._icon = ICON_TV_OFF

        self._supported_features = SUPPORT_SAMSUNGTV
        if self._config.method != 'legacy':
            self._supported_features |= SUPPORT_TURN_ON

        # Mark the end of a shutdown command (need to wait 15 seconds before
        # sending the next command to avoid turning the TV back ON).
        self._end_of_power_off = None

        # Mark the end of the TV powering on.need to wait 20 seconds before
        # sending any commands.
        self._end_of_power_on = None
        # Generate a configuration for the Samsung library

        self._remote = self._remote_class(self._config)

    def update(self):
        """Update state of device."""
        if self._power_off_in_progress():
            _LOGGER.debug(
                self._config.display_name + ' TV: Powering Off'
            )
            self._state = STATE_OFF
            self._icon = ICON_TV_OFF
            # self._entity_image = self._tv_image

        elif self._power_on_in_progress():
            _LOGGER.debug(
                self._config.display_name + ' TV: Powering On'
            )
            self._state = STATE_OFF
            self._icon = ICON_TV_OFF
            # self._entity_image = self._tv_image
        else:
            power = self._remote.power
            if power is True and self._remote.is_connected:
                self._config.save()

                if self._tv_image is None:
                    tv_image = self._remote.icon
                    if tv_image is not None:
                        self._tv_image = tv_image.data
                sources = self._remote.sources
                entity_image = self._tv_image
                source = 'Unknown'

                if sources is None:
                    if self._has_apps:
                        sources = [
                            'TV',
                            'HDMI'
                        ]

                        for app in self._remote.applications:

                            if app.is_running and app.is_visible:
                                source = 'APP: ' +app.name
                                entity_image = app.icon

                            sources += ['APP: ' + app.name]

                        self._sources = sources
                        self._source = source
                        self._entity_image = entity_image
                    else:
                        self._sources = [
                            'Source',
                            'Component 1',
                            'Component 2',
                            'AV 1',
                            'AV 2',
                            'AV 3',
                            'S Video 1',
                            'S Video 2',
                            'S Video 3',
                            'HDMI',
                            'HDMI 1',
                            'HDMI 2',
                            'HDMI 3',
                            'HDMI 4',
                            'FM-Radio',
                            'DVI',
                            'DVR',
                            'TV',
                            'Analog TV',
                            'Digital TV'
                        ]
                        self._key_source = True
                else:
                    new_sources = []
                    for src in sources:
                        if src.is_active:
                            if src.label != src.name:
                                source = src.label + ':' + src.name
                            else:
                                source = src.name

                        if src.name != src.label:
                            new_sources += [src.label + ':' + src.name]
                        else:
                            new_sources += [src.name]

                    self._key_source = False
                    self._sources = new_sources[:]

                self._source = source
                # self._entity_image = entity_image

                if self._source.upper().endswith('TV'):
                    self._icon = ICON_TV
                elif self._source.upper().endswith('USB'):
                    self._icon = ICON_USB
                elif self._source.upper().endswith('PC'):
                    self._icon = ICON_PC
                elif self._source.upper().endswith('DLNA'):
                    self._icon = ICON_DLNA

                elif 'S VIDEO' in self._source.upper():
                    self._icon = ICON_SVIDEO
                elif 'COMPONENT' in self._source.upper():
                    self._icon = ICON_COMPONENT
                elif 'AV' in self._source.upper():
                    self._icon = ICON_AV
                elif 'HDMI' in self._source.upper():
                    self._icon = ICON_HDMI
                elif 'YOUTUBE' in self._source.upper():
                    self._icon = ICON_YOUTUBE
                elif 'HULU' in self._source.upper():
                    self._icon = ICON_HULU
                elif 'NETFLIX' in self._source.upper():
                    self._icon = ICON_NETFLIX
                elif 'PLEX' in self._source.upper():
                    self._icon = ICON_PLEX
                elif 'SPOTIFY' in self._source.upper():
                    self._icon = ICON_SPOTIFY
                elif 'AMAZON' in self._source.upper():
                    self._icon = ICON_AMAZON
                elif 'PLAYSTATION' in self._source.upper():
                    self._icon = ICON_PLAYSTATION
                else:
                    self._icon = ICON_UNKNOWN

                volume = self._remote.volume
                _LOGGER.debug(
                    self._config.display_name + ' TV: Volume = ' + str(volume)
                )
                if volume is not None:
                    self._volume = volume / 100.0

                mute = self._remote.mute
                _LOGGER.debug(
                    self._config.display_name + ' TV: Mute = ' + str(mute)
                )
                if mute is None:
                    self._mute = False
                else:
                    self._mute = mute

                _LOGGER.debug(
                    self._config.display_name + ' TV: Power is On'
                )
                self._state = STATE_ON
            else:
                _LOGGER.debug(
                    self._config.display_name + ' TV: Power is Off'
                )
                # self._entity_image = self._tv_image
                self._icon = ICON_TV_OFF
                self._state = STATE_OFF

    def send_key(self, key):
        """Send a key to the tv and handles exceptions."""
        if self._power_off_in_progress():
            _LOGGER.info(
                self._config.display_name +
                " TV: powering off, not sending command: %s",
                key
            )
            return

        elif self._power_on_in_progress():
            _LOGGER.info(
                self._config.display_name +
                " TV: powering on, not sending command: %s",
                key
            )
            return

        if self._state == STATE_OFF:
            _LOGGER.info(
                self._config.display_name +
                " TV: powered off, not sending command: %s",
                key
            )
            return

        self._remote.control(key)

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def entity_picture(self):
        """Return the entity picture to use in the frontend, if any."""
        return self._entity_image

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the device."""
        return '{' + self._config.uuid + '}'

    @property
    def name(self):
        """Return the name of the device."""
        return self._config.display_name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return self._supported_features

    def select_source(self, source):
        """Select input source."""
        if self._key_source:
            if source == 'Analog TV':
                source = 'ANTENA'

            elif source == 'Digital TV':
                source = 'DTV'

            source = source.upper().replace('-', '_').replace(' ', '')
            source = 'KEY_' + source
            _LOGGER.debug(
                self._config.display_name + ' TV: changing source to ' + source
            )
            self.send_key(source)
        else:
            if 'APP' in source:
                app_name = source.rsplit(':', 1)[-1]
                app = self._remote.get_application(app_name)

                if app is not None:
                    app.run()

            if ':' in source:
                source = source.rsplit(':', 1)[-1]
            _LOGGER.debug(
                self._config.display_name + ' TV: changing source to ' + source
            )
            self._remote.source = source

    @property
    def source(self):
        """Name of the current input source."""
        return self._source

    @property
    def source_list(self):
        """List of available input sources."""
        return self._sources

    def volume_up(self):
        """Volume up the media player."""
        self.send_key('KEY_VOLUP')

    def volume_down(self):
        """Volume down media player."""
        self.send_key('KEY_VOLDOWN')

    @property
    def volume_level(self):
        """Volume level of the media player scalar volume. 0.0-1.0."""
        return self._volume

    def set_volume_level(self, volume):
        """Set volume level, convert scalar volume. 0.0-1.0 to percent 0-100"""
        self._remote.volume = int(volume * 100)

    def mute_volume(self, mute):
        """Send mute command."""
        self._remote.mute = mute

    @property
    def is_volume_muted(self):
        """Boolean if volume is currently muted."""
        return self._mute

    def media_play_pause(self):
        """Simulate play pause media player."""
        if self._playing:
            self.media_pause()
        else:
            self.media_play()

    def media_play(self):
        """Send play command."""
        self._playing = True
        self.send_key('KEY_PLAY')

    def media_pause(self):
        """Send media pause command to media player."""
        self._playing = False
        self.send_key('KEY_PAUSE')

    def media_next_track(self):
        """Send next track command."""
        self.send_key('KEY_FF')

    def media_previous_track(self):
        """Send the previous track command."""
        self.send_key('KEY_REWIND')

    async def async_play_media(self, media_type, media_id, **kwargs):
        """Support changing a channel."""
        if media_type != MEDIA_TYPE_CHANNEL:
            _LOGGER.error(
                self._config.display_name + ' TV: Unsupported media type'
            )
            return

        # media_id should only be a channel number
        try:
            cv.positive_int(media_id)
        except vol.Invalid:
            _LOGGER.error(
                self._config.display_name +
                ' TV: Media ID must be positive integer'
            )
            return

        for digit in media_id:
            await self.hass.async_add_job(self.send_key, 'KEY_' + digit)
            await asyncio.sleep(KEY_PRESS_TIMEOUT, self.hass.loop)

    @property
    def app_id(self):
        """ID of the current running app."""
        return None

    @property
    def app_name(self):
        """Name of the current running app."""
        return None

    def turn_on(self):
        """Turn the media player on."""

        if self._power_on_in_progress():
            return

        if self._config.mac:
            self._end_of_power_on = dt_util.utcnow() + timedelta(seconds=20)

            if self._power_off_in_progress():
                self._end_of_power_on += (
                    dt_util.utcnow() - self._end_of_power_off
                )

            def do():
                _LOGGER.debug(
                    self._config.display_name + ' TV: Power on process started'
                )
                event = threading.Event()
                while self._power_off_in_progress():
                    event.wait(0.5)

                self._remote.power = True

            t = threading.Thread(target=do)
            t.daemon = True
            t.start()
        elif self._config.method != 'legacy':
            _LOGGER.info(
                self._config.display_name +
                " TV: There was a problem detecting the TV's MAC address, "
                "you will have to update the MAC address in the Home "
                "Assistant config file manually."
            )

        else:
            _LOGGER.info(
                self._config.display_name +
                " TV: Legacy TV's (2008 - 2013) do not support "
                "being powered on remotely."
            )

    def _power_on_in_progress(self):
        return (
            self._end_of_power_on is not None and
            self._end_of_power_on > dt_util.utcnow()
        )

    def turn_off(self):
        """Turn off media player."""

        if self._power_off_in_progress():
            return

        self._end_of_power_off = dt_util.utcnow() + timedelta(seconds=15)

        if self._power_on_in_progress():
            self._end_of_power_off += (
                dt_util.utcnow() - self._end_of_power_on
            )

        def do():
            _LOGGER.debug(
                self._config.display_name + ' TV: Power off process started'
            )
            event = threading.Event()
            while self._power_on_in_progress():
                event.wait(0.5)

            self._remote.power = False

        t = threading.Thread(target=do)
        t.daemon = True
        t.start()

    def _power_off_in_progress(self):
        return (
            self._end_of_power_off is not None and
            self._end_of_power_off > dt_util.utcnow()
        )