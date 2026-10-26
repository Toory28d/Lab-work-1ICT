"""Atomic JSON persistence shared by API and worker."""
import json
import os
import tempfile
from pathlib import Path

BASE = Path(os.environ.get('LAB2_DATA_DIR', Path(__file__).resolve().parent / 'data'))
QUEUE = BASE / 'queue'
PROCESSING = BASE / 'processing'
TASKS = BASE / 'tasks'


def init_dirs():
    for directory in (QUEUE, PROCESSING, TASKS):
        directory.mkdir(parents=True, exist_ok=True)


def write_json(path, value):
    init_dirs()
    fd, temp = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as file:
            json.dump(value, file, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def read_json(path):
    with open(path, encoding='utf-8') as file:
        return json.load(file)
