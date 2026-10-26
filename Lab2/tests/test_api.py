import importlib
import json
import sys
import time
from pathlib import Path
import pytest


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setenv('LAB2_DATA_DIR', str(tmp_path))
    for name in ('storage', 'app', 'worker'):
        sys.modules.pop(name, None)
    api = importlib.import_module('app')
    worker = importlib.import_module('worker')
    return api.app.test_client(), worker, tmp_path


def test_message(setup):
    client, _, _ = setup
    assert client.get('/api/message').json['message']


def test_time(setup):
    client, _, _ = setup
    assert '+00:00' in client.get('/api/time').json['utc_time']


@pytest.mark.parametrize('data', [None, {}, {'text': ''}, {'text': 3}, {'text': 'x'*201}, {'text':'ok','extra':1}, []])
def test_bad_inputs(setup, data):
    client, _, _ = setup
    response = client.post('/api/tasks', json=data)
    assert response.status_code == 400 and 'error' in response.json


def test_wrong_content_type(setup):
    client, _, _ = setup
    assert client.post('/api/tasks', data='abc').status_code == 400


def test_missing_task(setup):
    client, _, _ = setup
    assert client.get('/api/tasks/not-a-uuid').status_code == 404


def test_queue_worker_result(setup):
    client, worker, _ = setup
    response = client.post('/api/tasks', json={'text': 'hello world'})
    assert response.status_code == 202
    task_id = response.json['task_id']
    assert client.get('/api/tasks/'+task_id).json['status'] == 'queued'
    assert worker.process_one()
    record = client.get('/api/tasks/'+task_id).json
    assert record['status'] == 'completed' and record['result'] == 'HELLO WORLD'


def test_ten_jobs(setup):
    client, worker, _ = setup
    ids = [client.post('/api/tasks', json={'text':f'job {i}'}).json['task_id'] for i in range(10)]
    start = time.monotonic()
    while time.monotonic() - start < 15 and any(client.get('/api/tasks/'+i).json['status'] != 'completed' for i in ids):
        worker.process_one()
    assert all(client.get('/api/tasks/'+i).json['status'] == 'completed' for i in ids)


def test_recover_claimed_message(setup):
    client, worker, base = setup
    task_id = client.post('/api/tasks', json={'text':'recover'}).json['task_id']
    (base/'queue'/f'{task_id}.json').rename(base/'processing'/f'{task_id}.json')
    worker.recover()
    assert worker.process_one()
    assert client.get('/api/tasks/'+task_id).json['result'] == 'RECOVER'
