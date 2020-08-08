"""
Thermostat night script
"""
@service
def test():
    if binary_sensor.workday == 'on':
        log.info(f"State Trigger test: fail")
        pass
    else:
        log.info(f"State Trigger test: pass")
        pass