# Lab 2 — REST API + asynchronous file queue

Python Flask API and a separate file-queue worker. The service processes a submitted text by converting it to uppercase.

## Setup (PowerShell)
```powershell
cd Lab2
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run (two terminals)
Terminal 1:
```powershell
python app.py
```
Terminal 2:
```powershell
python worker.py
```

## Try the API (PowerShell)
```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/message
Invoke-RestMethod http://127.0.0.1:5000/api/time
$task = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/tasks -ContentType 'application/json' -Body '{"text":"hello world"}'
$task
Invoke-RestMethod "http://127.0.0.1:5000/api/tasks/$($task.task_id)"
```
Stop the worker, submit a new task, and check that it stays `queued`; restart worker and check that it becomes `completed`.

## Test
```powershell
python -m pytest tests/ -v
python tests/check_latency.py
```

## Files
- `spec.md` — requirements and API contract
- `app.py` — HTTP endpoints
- `worker.py` — background consumer
- `storage.py` — atomic JSON file operations
- `data/` — runtime queue and state (ignored by Git)
- `report.pdf` — technical report; `screenshots/` — add screenshots from your own live demonstration

## Git history requirement
The instructor requires the initial specification to be committed **before** implementation. Commit `spec.md` alone first, then commit the code and documentation. A single bulk commit cannot demonstrate this requirement.

## Security
Do not commit AWS keys, `.env`, `.venv`, or runtime data. No AWS account is required for the file-queue option.
