"""
tag event trigger test script
"""
@event_trigger('tag_scanned') 
def handle_scanned_tag(tag_id=None, device_id=None, context=None):
    log.info(f"got tag_scanned with tag_id={tag_id}, device_id={device_id}, user_id={context.user_id}")
    if tag_id == "41220ee3-400d-480e-85df-314426688b99": 
        scene.turn_on(entity_id="scene.merry_christmas", transition="0")
        