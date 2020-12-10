@event_trigger("my_event")
def got_my_event(**kwargs):
    log.info(f"got my_event: kwargs={kwargs}")