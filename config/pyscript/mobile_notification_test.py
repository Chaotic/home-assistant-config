"""
notification event trigger test script
"""
@event_trigger("mobile_app_notification_action")
def handle_notification_action(**kwargs):
    log.info(f"got mobile_app_notification_action with kwargs={kwargs}")