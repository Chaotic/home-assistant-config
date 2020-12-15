"""
Control the Master Closet lights with motions
"""
@state_trigger("binary_sensor.bosch_isw_zpr1_wp13_b44cc385_5_1280 == 'on'")
@time_active("range(05:30, 23:00)")
def closet_motion_day():
    log.info(f"closet on day:")
    light.turn_on(entity_id="group.master_bedroom_closet",brightness=255)

@state_trigger("binary_sensor.bosch_isw_zpr1_wp13_b44cc385_5_1280 == 'on'")
@time_active("range(23:00, 5:30)")
def closet_motion_night():
    log.info(f"closet on night")
    light.turn_on(entity_id="group.master_bedroom_closet",brightness=50)

@state_trigger("binary_sensor.bosch_isw_zpr1_wp13_b44cc385_5_1280 == 'on'")
def closet_motion_off():
    trig_info = task.wait_until(
                    state_trigger="group.device_trackers == 'home'",
                    timeout=120
                )
    if trig_info["trigger_type"] == "timeout":
        pass
    else:
        log.info(f"closet off")
        light.turn_off(entity_id="group.master_bedroom_closet")
