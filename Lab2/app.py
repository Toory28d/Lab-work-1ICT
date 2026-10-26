"""Lab 2 REST API. Run: python app.py"""
from datetime import datetime, timezone
from uuid import uuid4
from flask import Flask, jsonify, request
from storage import QUEUE, TASKS, init_dirs, read_json, write_json

app = Flask(__name__)
init_dirs()


def now():
    return datetime.now(timezone.utc).isoformat()


@app.get('/api/message')
def message():
    return jsonify(message='Hello from Lab 2 REST API')


@app.get('/api/time')
def time_now():
    return jsonify(utc_time=now())


@app.post('/api/tasks')
def submit_task():
    if not request.is_json:
        return jsonify(error='Content-Type must be application/json'), 400
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or set(payload) != {'text'}:
        return jsonify(error='JSON must contain only the text field'), 400
    value = payload['text']
    if not isinstance(value, str) or not (1 <= len(value.strip()) <= 200):
        return jsonify(error='text must be a nonempty string of at most 200 characters'), 400
    task_id = str(uuid4())
    record = dict(task_id=task_id, status='queued', result=None, error=None, created_at=now())
    write_json(TASKS / f'{task_id}.json', record)
    write_json(QUEUE / f'{task_id}.json', dict(task_id=task_id, text=value, created_at=record['created_at']))
    return jsonify(task_id=task_id, status='queued'), 202


@app.get('/api/tasks/<task_id>')
def task_status(task_id):
    from uuid import UUID
    try:
        if str(UUID(task_id)) != task_id:
            raise ValueError()
    except ValueError:
        return jsonify(error='Task not found'), 404
    path = TASKS / f'{task_id}.json'
    if not path.is_file():
        return jsonify(error='Task not found'), 404
    return jsonify(read_json(path))


@app.errorhandler(404)
def not_found(_):
    return jsonify(error='Endpoint not found'), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify(error='Method not allowed'), 405


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
