"""
State trigger test script
"""
@state_trigger("group.device_trackers == 'not_home'")
def state_trigger():
    log.info(f"State Trigger test:")
    trig_info = task.wait_until(
                    state_trigger="group.device_trackers == 'home'",
                    timeout=120
                )
    if trig_info["trigger_type"] == "timeout":
        log.info(f"State Trigger test: fail")
        pass
    else:
        log.info(f"State Trigger test: pass")
        pass