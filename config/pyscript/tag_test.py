"""
tag event trigger test script
"""
@event_trigger('tag_scanned') 
def handle_scanned_tag(tag_id=None, device_id=None, context=None):
    log.info(f"got tag_scanned with tag_id={tag_id}, device_id={device_id}, user_id={context.user_id}")
    if tag_id == "69086949-ee9c-4512-a55f-b2fdbec2b1f3": 
        log.info(f"got the right tag")
        if context.user_id == "2e85aebd0a9c436c8567c5435f0d0df8":
            log.info(f"Matt Scanned")
            light.turn_on(entity_id="light.matt_night_light", brightness=255)
        elif context.user_id == "2a87a65d647c45bdac0c64045a92fa55":
            log.info(f"Kedar Scanned")
            light.turn_on(entity_id="light.kedar_night_light", brightness=255)
        