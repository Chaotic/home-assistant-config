"""
Thermostat night script
"""
@time_trigger("once(23:00:00)")
def thermostat_night():
    """Trigger at 11pm every night"""
    if input_boolean.vacation != 'on':
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
    elif input_boolean.vacation == 'on':
        """Set High Temp"""
        hightemp = 85
        """Set Low Temp"""
        lowtemp = 55
        """Send the actual command to the thermostat"""
    climate.set_temperature(entity_id="climate.thermostat_2",target_temp_low=lowtemp,target_temp_high=hightemp,hvac_mode="heat_cool")
