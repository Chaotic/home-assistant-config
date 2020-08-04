"""
Thermostat test script
"""
@time_trigger(once(23:00:00))
def Thermostat Night():
    """Trigger at 11pm every test example using pyscript."""
    log.info(f"Time Trigger:")
    if sensor.dark_sky_daytime_high_temperature_0d > 85:
    	log.info(f"greater than 85:")
	elif sensor.dark_sky_daytime_high_temperature_0d < 85:
    	log.info(f"less than 85:")
    