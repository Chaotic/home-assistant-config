"""
shut Henry's Internet off at night
"""
@time_trigger("once(09:00:00)")
def henry_computer_school_on():
    if binary_sensor.workday == 'on':
        """Trigger at 9:00am every morning"""
        homeassistant.turn_on(entity_id="switch.henry_s_computer")

@time_trigger("once(06:30:00)")
def henry_computer_nonschool_on():
    if binary_sensor.workday != 'on':
        """Trigger at 3:30am every morning"""
        homeassistant.turn_on(entity_id="switch.henry_s_computer")
