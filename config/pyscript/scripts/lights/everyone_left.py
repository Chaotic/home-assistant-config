"""
Thermostat occupancy script
"""
@state_trigger("group.device_trackers == 'not_home'")
def themostat_left():
    trig_info = task.wait_until(
                    state_trigger="group.device_trackers == 'home'",
                    timeout=600
                )
    if trig_info["trigger_type"] == "timeout":
        pass
    else:
        if input_boolean.guest_mode == "on":
            pass
        elif input_boolean.guest_mode == "off":
            homeassistant.off(entity_id="group.all_lights_custom")
        pass