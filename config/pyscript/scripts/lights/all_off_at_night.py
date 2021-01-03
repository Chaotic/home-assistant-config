"""
shut everything off at night
"""
@time_trigger("once(23:00:00)")
def all_lights_off():
    """Trigger at 11:00pm every night"""
    homeassistant.turn_off(entity_id="group.all_lights_custom")

@time_trigger("once(1:00:00)")
def all_lights_off2():
    """Trigger at 11:00pm every night"""
    homeassistant.turn_off(entity_id="group.all_lights_custom")