"""
Time trigger test script
"""
@time_trigger("once(17:15:00)")
def thermostat_night():
    """Trigger at 6pm every test example using pyscript."""
    log.info(f"Time Trigger test:")

