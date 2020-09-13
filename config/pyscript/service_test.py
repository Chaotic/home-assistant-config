"""
Service test script
"""
@service
def test():
    if input_boolean.vacation == 'on':
        log.warning(f"Service Trigger test: fail")
        pass
    else:
        log.warning(f"Service Trigger test: pass")
        pass