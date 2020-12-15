"""
Control the outside lights.
"""
@time_trigger("once(sunrise + 45m)")
def outside_lights_off():
    """Trigger at 45 mins before sunrise every morning"""
    homeassistant.off(entity_id="group.outside_lights")

@time_trigger("once(sunset - 45m)")
def outside_lights_on():
    """Trigger at 45 mins before sunset every night"""
    homeassistant.on(entity_id="group.outside_lights")
