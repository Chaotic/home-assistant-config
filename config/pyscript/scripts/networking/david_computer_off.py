"""
shut David's Internet off at night
"""
@time_trigger("once(19:30:00)")
def david_computer_school_off():
    if binary_sensor.workday == 'on':
        """Trigger at 7:30pm every night"""
        homeassistant.turn_off(entity_id="switch.david_s_computer")

@time_trigger("once(20:30:00)")
def david_computer_nonschool_off():
    if binary_sensor.workday != 'on':
        """Trigger at 8:30pm every night"""
        homeassistant.turn_off(entity_id="switch.david_s_computer")
