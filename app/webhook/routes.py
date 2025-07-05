from flask import Blueprint, request, jsonify, render_template
from app.models import WebhookEvent
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/webhook/receiver', methods=['POST'])
def webhook_receiver():
    try:
        payload = request.get_json()
        event_type = request.headers.get('X-GitHub-Event')

        event_data = parse_webhook(payload, event_type)

        if event_data:
            WebhookEvent.save_event(
                request_id=event_data['request_id'],
                author=event_data['author'],
                action=event_data['action'],
                timestamp=event_data['timestamp'],
                from_branch=event_data.get('from_branch'),
                to_branch=event_data.get('to_branch')
            )

            return jsonify({'message': 'Webhook received successfully'}), 200
        else:
            return jsonify({'message': 'Event not tracked'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/events', methods=['GET'])
def get_events():
    try:
        events = WebhookEvent.get_latest_events()
        return jsonify(events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def parse_webhook(payload, event_type):
    """Parse GitHub webhook payload"""
    try:
        timestamp = datetime.utcnow().isoformat()

        if event_type == 'push':
            return {
                'request_id': payload.get('head_commit', {}).get('id', '')[:8],
                'author': payload.get('head_commit', {}).get('author', {}).get('name', 'Unknown'),
                'action': 'push',
                'timestamp': timestamp,
                'to_branch': payload.get('ref', '').replace('refs/heads/', ''),
                'from_branch': None
            }

        elif event_type == 'pull_request':
            pr = payload.get('pull_request', {})
            action = payload.get('action', '')

            # Check if this is a merge event
            if action == 'closed' and pr.get('merged'):
                return {
                    'request_id': str(pr.get('number', '')),
                    'author': pr.get('user', {}).get('login', 'Unknown'),
                    'action': 'merge',
                    'timestamp': timestamp,
                    'from_branch': pr.get('head', {}).get('ref', ''),
                    'to_branch': pr.get('base', {}).get('ref', '')
                }
            else:
                return {
                    'request_id': str(pr.get('number', '')),
                    'author': pr.get('user', {}).get('login', 'Unknown'),
                    'action': 'pull_request',
                    'timestamp': timestamp,
                    'from_branch': pr.get('head', {}).get('ref', ''),
                    'to_branch': pr.get('base', {}).get('ref', '')
                }

        return None

    except Exception:
        return None