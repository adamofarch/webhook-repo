from pymongo import MongoClient
from datetime import datetime
mongo = MongoClient("mongodb://localhost:27017/test_db")

def convert_iso_to_display_format(iso_timestamp):
    dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))

    utc_dt = dt.utctimetuple()
    utc_datetime = datetime(*utc_dt[:6])

    day = utc_datetime.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    formatted = utc_datetime.strftime(f"%d{suffix} %B %Y - %I:%M %p UTC")

    return formatted

def parse_github_event(payload, event_type):
    if event_type == 'push':
        timestamp = payload.get('head_commit', {}).get('timestamp')
        formatted_timestamp = convert_iso_to_display_format(timestamp) if timestamp else None
        return {
            'action': 'PUSH',
            'request_id': payload.get('head_commit', {}).get('id'),
            'repository': payload.get('repository', {}).get('name'),
            'author': payload.get('pusher', {}).get('name'),
            'to_branch': payload.get('ref', '').replace('refs/heads/', ''),
            'timestamp': formatted_timestamp,
        }
    elif event_type == 'pull_request' and payload.get('action') in ['opened', 'reopened']:
        timestamp = payload.get('pull_request', {}).get('updated_at')
        formatted_timestamp = convert_iso_to_display_format(timestamp) if timestamp else None
        return {
            'action': 'PULL_REQUEST',
            'author': payload.get('pull_request', {}).get('user', {}).get('login'),
            'request_id': str(payload.get('pull_request', {}).get('id')),
            'from_branch': payload.get('pull_request', {}).get('head', {}).get('ref'),
            'to_branch': payload.get('pull_request', {}).get('base', {}).get('ref'),
            'timestamp': formatted_timestamp,
        }

    elif event_type == 'pull_request' and payload.get('action') == 'closed' and payload.get('pull_request', {}).get('merged'):
        timestamp = payload.get('pull_request', {}).get('merged_at')
        formatted_timestamp = convert_iso_to_display_format(timestamp) if timestamp else None
        return {
            'action': 'MERGE',
            'author': payload.get('pull_request', {}).get('user', {}).get('login'),
            'request_id': payload.get('pull_request').get('merge_commit_sha'),
            'from_branch': payload.get('pull_request', {}).get('head', {}).get('ref'),
            'to_branch': payload.get('pull_request', {}).get('base', {}).get('ref'),
            'timestamp': formatted_timestamp,
        }
    return None

def push_to_mongo(event_data):
    if event_data:
        try:
            response = mongo.test_db.events_data.insert_one(event_data)
            print(response)
            return f"Event saved to MongoDB: {event_data}"
        except Exception as e:
            return f"Error saving event to MongoDB: {e}"
    else:
        return "No event data to save."
