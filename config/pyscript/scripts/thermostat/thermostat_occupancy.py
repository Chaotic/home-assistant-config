"""
Thermostat occupancy script
"""
@state_trigger("group.device_trackers == 'not_home'")
def themostat_left():
    trig_info = task.wait_until(
                    state_trigger="group.device_trackers == 'not_home'",
                    state_hold=600,
                )
    if trig_info["trigger_type"] == "timeout":
        pass
    else:
        """Set High Temp"""
        if float(sensor.average_weather_high_temperature) > 85.0:
            hightemp = 85
        elif float(sensor.average_weather_high_temperature) < 85.0:
            hightemp = 85
        """Set Low Temp"""
        if float(sensor.average_weather_low_temperature) > 50.0:
            lowtemp = 55
        elif float(sensor.average_weather_low_temperature) < 50.0:
            lowtemp = 55
        """Send the actual command to the thermostat"""
        climate.set_temperature(entity_id="climate.thermostat_2",target_temp_low=lowtemp,target_temp_high=hightemp,hvac_mode="heat_cool")
        pass

@state_trigger("group.device_trackers == 'home'")
def themostat_returned():
    trig_info = task.wait_until(
                    state_trigger="group.device_trackers == 'home'",
                    timeout=30
                )
    if trig_info["trigger_type"] == "timeout":
        pass
    else:
        """Set High Temp"""
        if float(sensor.average_weather_high_temperature) > 85.0:
            hightemp = 75
        elif float(sensor.average_weather_high_temperature) < 85.0:
            hightemp = 85
        """Set Low Temp"""
        if float(sensor.average_weather_low_temperature) > 50.0:
            lowtemp = 55
        elif float(sensor.average_weather_low_temperature) < 50.0:
            lowtemp = 65
        """Send the actual command to the thermostat"""
        climate.set_temperature(entity_id="climate.thermostat_2",target_temp_low=lowtemp,target_temp_high=hightemp,hvac_mode="heat_cool")
        pass
