from datetime import datetime
from app.extensions import mongo


class WebhookEvent:
    @staticmethod
    def save_event(request_id, author, action, timestamp, from_branch=None, to_branch=None):
        event = {
            'request_id': request_id,
            'author': author,
            'action': action,
            'timestamp': timestamp,
            'from_branch': from_branch,
            'to_branch': to_branch
        }
        return mongo.db.webhook_events.insert_one(event)

    @staticmethod
    def get_latest_events(limit=20):
        return list(mongo.db.webhook_events.find().sort('timestamp', -1).limit(limit))