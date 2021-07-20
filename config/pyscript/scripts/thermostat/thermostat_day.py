"""
Thermostat day script
"""
@time_trigger("once(6:30:00)")
def thermostat_work_day():
    """Trigger at 7:30am every"""
    """Only trigger on workday"""
    if input_boolean.vacation != 'on':
        if binary_sensor.workday == 'on':
            """Set High Temp"""
            if float(sensor.average_weather_high_temperature) > 85.0:
                hightemp = 75
            elif float(sensor.average_weather_high_temperature) < 85.0:
                hightemp = 85
            """Set Low Temp"""
            if float(sensor.average_weather_low_temperature) > 50.0:
                lowtemp = 55
            elif float(sensor.average_weather_low_temperature) < 50.0:
                lowtemp = 68
            """Send the actual command to the thermostat"""
            climate.set_temperature(entity_id="climate.thermostat_2",target_temp_low=lowtemp,target_temp_high=hightemp,hvac_mode="heat_cool")

@time_trigger("once(7:30:00)")
def thermostat_nonwork_day():
    """Trigger at 8:30am every"""
    if input_boolean.vacation != 'on':
        if binary_sensor.workday != 'on':
            """Set High Temp"""
            if float(sensor.average_weather_high_temperature) > 85.0:
                hightemp = 75
            elif float(sensor.average_weather_high_temperature) < 85.0:
                hightemp = 85
            """Set Low Temp"""
            if float(sensor.average_weather_low_temperature) > 50.0:
                lowtemp = 55
            elif float(sensor.average_weather_low_temperature) < 50.0:
                lowtemp = 68
            """Send the actual command to the thermostat"""
            climate.set_temperature(entity_id="climate.thermostat_2",target_temp_low=lowtemp,target_temp_high=hightemp,hvac_mode="heat_cool")
