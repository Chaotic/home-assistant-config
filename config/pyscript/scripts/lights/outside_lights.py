"""
Control the outside lights.
"""
@time_trigger("once(sunrise + 45m)")
def outside_lights_off():
    """Trigger at 45 mins before sunrise every morning"""
    homeassistant.turn_off(entity_id="group.outside_lights")

@time_trigger("once(sunset - 45m)")
def outside_lights_on():
    """Trigger at 45 mins before sunset every night"""
    homeassistant.turn_on(entity_id="group.outside_lights")
