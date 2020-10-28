"""
State trigger test script
"""
@event_trigger('tag_scanned') 
def handle_scanned_tag(**kwargs):
    log.info(f"got tag_scanned with kwargs={kwargs}")