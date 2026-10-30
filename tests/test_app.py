import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app


def test_home():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Hello from Lab 3!'
        assert data['hostname']
        assert data['timestamp']


def test_health():
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert response.get_json()['status'] == 'ok'


def test_info():
    with app.test_client() as client:
        response = client.get('/info')
        assert response.status_code == 200
        assert response.get_json()['version'] == '1.0'


def test_unknown_route():
    with app.test_client() as client:
        assert client.get('/missing').status_code == 404
