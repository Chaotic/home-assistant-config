# ChaoicUnreal's Home Assistant Config

This is the config for my active home assistant system.  This setup is heavily inspired by [Frenck's Home Assistant Config](https://github.com/frenck/home-assistant-config).

Everything is set up in its own file so that I can more easily add/remove components.

I'm still in the process of setting everything up part of which is putting on every possible component that seems interesting and figuring out what I want to actually keep.

## Deployment

Copy the config files and recreate the secrets.yaml file Also you need the same hardware I have.

## Hardware
   
<b>Plugs</b>
    Wemo mini plugs (wifi),
    Gosund (wifi) (not in use yet)

<b>Lights</b>
    Sengled Light bulbs (Zigbee)

<b>Switches</b>
    Zooz dimmer switches (Z-wave)

<b>Sensors</b>
   Bosch Motion sensors (Zigbee),
   Zooz 4-in-1 sensors (Z-wave),
   smartthings door sensor (Zigbee)

<b>Speakers</b>
   Sonos speakers (wifi)

<b>Media Players</b>
   Chromecast (wifi),
   Samsung Smart TV (wifi)

<b>Thermostat</b>
   Radio Thermostat Z-Wave CT101 (Really cheap z-wave thermostat)

<b>Other</b>
   Xiaomi Smart Cube (Zigbee),
   SmartThings Hub (Wired),
   Tomato Router (Wired)

## Software
   SmartThings to MQTT Bridge,
   Plex Media Server,
   MQTT Broker,
   Owntracks,
   qBittorrent,
   Transmission,
   MariaDB,
   Tautulli
   InfluxDB
   Grafana
   
## Other Components
These are various Components that don't directly link to hardware/software

   Pushbullet (notifications),
   ISS (virtual sensors for if the ISS is overhead),
   Workday (virtual sensor for if it's a workday),
   Waze (travel time),
   WAke on Lan (let me wake up other computers),
   Launch (Next space launch),
   Moon (Moon phases),
   Sun (Sunrise),
   Season (lets me know the season),
   yr (Weather),
   Google TTS (Text to Speech),
   Dark Sky (Weather)


## Authors

* **ChaoticUnreal** - Its my house

## Acknowledgments

Heavily inspired by [Frenck's config](https://github.com/frenck/home-assistant-config)  (some of the basic stub files were copied directly)