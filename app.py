import os
import socket
from datetime import datetime, timezone
from flask import Flask, jsonify

app = Flask(__name__)

@app.get('/')
def home():
    return jsonify(message='Hello from Lab 3!', hostname=socket.gethostname(), timestamp=datetime.now(timezone.utc).isoformat())

@app.get('/health')
def health():
    return jsonify(status='ok'), 200

@app.get('/info')
def info():
    return jsonify(service='lab3-flask-api', hostname=socket.gethostname(), version='1.0', environment=os.getenv('APP_ENV', 'local'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
