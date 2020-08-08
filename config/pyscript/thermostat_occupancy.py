"""
Thermostat occupancy script
"""
@state_trigger("group.device_trackers == 'not_home'")
def themostat_left():
    log.info(f"Everyone Left now Waiting for 2 mins")
    trig_info = task.wait_until(
                    state_trigger="group.device_trackers == 'home'",
                    timeout=120
                )
    if trig_info["trigger_type"] == "timeout":
        log.info(f"Everyone left but came back in 2 mins:")
        pass
    else:
        log.info(f"Everyone left forever:")
        """Set High Temp"""
        if float(sensor.dark_sky_daytime_high_temperature_0d) > 85.0:
            hightemp = 85
        elif float(sensor.dark_sky_daytime_high_temperature_0d) < 85.0:
            hightemp = 85
        """Set Low Temp"""
        if float(sensor.dark_sky_overnight_low_temperature_0d) > 50.0:
            lowtemp = 55
        elif float(sensor.dark_sky_overnight_low_temperature_0d) < 50.0:
            lowtemp = 65
        """Send the actual command to the thermostat"""
        climate.set_temperature(entity_id="climate.radio_thermostat_company_of_america_ct101_thermostat_iris_mode",target_temp_low=lowtemp,target_temp_high=hightemp,hvac_mode="heat_cool")
        pass

@state_trigger("group.device_trackers == 'home'")
def themostat_left():
    log.info(f"Someone is home Waiting for 30 seconds")
    trig_info = task.wait_until(
                    state_trigger="group.device_trackers == 'not_home'",
                    timeout=30
                )
    if trig_info["trigger_type"] == "timeout":
        log.info(f"Everyone left within 30 seconds:")
        pass
    else:
        log.info(f"Everyone back forever:")
        """Set High Temp"""
        if float(sensor.dark_sky_daytime_high_temperature_0d) > 85.0:
            hightemp = 85
        elif float(sensor.dark_sky_daytime_high_temperature_0d) < 85.0:
            hightemp = 75
        """Set Low Temp"""
        if float(sensor.dark_sky_overnight_low_temperature_0d) > 50.0:
            lowtemp = 55
        elif float(sensor.dark_sky_overnight_low_temperature_0d) < 50.0:
            lowtemp = 65
        """Send the actual command to the thermostat"""
        climate.set_temperature(entity_id="climate.radio_thermostat_company_of_america_ct101_thermostat_iris_mode",target_temp_low=lowtemp,target_temp_high=hightemp,hvac_mode="heat_cool")
        pass
