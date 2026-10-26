"""File-queue worker. Run: python worker.py"""
import argparse
import os
import time
from datetime import datetime, timezone
from storage import QUEUE, PROCESSING, TASKS, init_dirs, read_json, write_json


def now():
    return datetime.now(timezone.utc).isoformat()


def recover():
    init_dirs()
    for path in PROCESSING.glob('*.json'):
        destination = QUEUE / path.name
        if not destination.exists():
            os.replace(path, destination)


def process_one():
    init_dirs()
    for source in sorted(QUEUE.glob('*.json')):
        claimed = PROCESSING / source.name
        try:
            os.rename(source, claimed)
        except (FileNotFoundError, FileExistsError):
            continue
        try:
            msg = read_json(claimed)
            state_path = TASKS / f"{msg['task_id']}.json"
            state = read_json(state_path)
            if state['status'] != 'completed':
                state['status'] = 'processing'
                state['updated_at'] = now()
                write_json(state_path, state)
                state['result'] = msg['text'].upper()
                state['status'] = 'completed'
                state['updated_at'] = now()
                write_json(state_path, state)
            claimed.unlink()
        except Exception as exc:
            try:
                state = read_json(state_path)
                state.update(status='failed', error=str(exc), updated_at=now())
                write_json(state_path, state)
                claimed.unlink(missing_ok=True)
            except Exception:
                # Preserve the message for recovery if persistence itself fails.
                pass
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='Process one available task and exit')
    args = parser.parse_args()
    recover()
    if args.once:
        process_one()
        return
    print('Worker started; press Ctrl+C to stop', flush=True)
    try:
        while True:
            if not process_one():
                time.sleep(0.2)
    except KeyboardInterrupt:
        print('Worker stopped')


if __name__ == '__main__':
    main()
