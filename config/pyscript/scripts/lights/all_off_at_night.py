"""
shut everything off at night
"""
@time_trigger("once(23:00:00)")
def all_lights_off():
    """Trigger at 11:00pm every night"""
    homeassistant.off(entity_id="group.all_lights_custom")
