"""
shut David's Internet on at morning
"""
@time_trigger("once(09:00:00)")
def david_computer_school_on():
    if binary_sensor.workday == 'on':
        """Trigger at 9:00am every morning"""
        homeassistant.turn_on(entity_id="switch.david_s_computer")

@time_trigger("once(06:30:00)")
def david_computer_nonschool_on():
    if binary_sensor.workday != 'on':
        """Trigger at 6:30am every morning"""
        homeassistant.turn_on(entity_id="switch.david_s_computer")
