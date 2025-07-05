from flask import Blueprint, json, request, jsonify
from app.extensions import mongo, parse_github_event, push_to_mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    try:
        payload = request.json
        headers = request.headers
        event_type = headers.get('X-GitHub-Event')        
        
        event_data = parse_github_event(payload, event_type)
        if event_data:
            push_to_mongo(event_data)

        return jsonify({'status': 'success', 'event_type': event_type}), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@webhook.route('/events')
def events():
    try:
        data = mongo.test_db.events_data.find()
        data = list(data)
        for item in data:
            item['_id'] = str(item['_id'])

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    if not data:
        return jsonify({'status': 'error', 'message': 'No events found'}), 404

    for item in data:
        item['_id'] = str(item['_id'])
    data = {'events': data}

    return json.dumps(data), 200
