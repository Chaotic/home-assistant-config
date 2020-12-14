"""
Reset some booleans at night.
"""
#@time_trigger("once(23:00:00)")
@service
def reset_night():
    """Trigger at 11:00pm every night"""
    homeassistant.off(entity_id="input_boolean.movie_mode")
    homeassistant.off(entity_id="input_boolean.snow_day")
