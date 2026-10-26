# Lab 2 — REST API and File Queue Specification (v1)

## Purpose
A small task-processing service accepts JSON jobs over HTTP, persists them in a filesystem queue, and processes them asynchronously using a separate worker process.

## Functional requirements
- **R1** `GET /api/message` returns a JSON greeting and HTTP 200.
- **R2** `GET /api/time` returns current UTC time in ISO-8601 format and HTTP 200.
- **R3** `POST /api/tasks` validates JSON with `text` (nonempty string, 1–200 chars), persists a task, and returns task ID, status `queued`, and HTTP 202.
- **R4** `GET /api/tasks/{task_id}` returns the status and result of a task, or HTTP 404 for an unknown ID.
- **R5** A separate worker consumes queued tasks, converts their text to uppercase, saves the result, then acknowledges/removes the queued message.
- **R6** Invalid JSON, wrong content type, missing/invalid fields, and unsupported task IDs return structured 400/404 errors without crashing the service.

## API contract
| Method | Endpoint | Input | Output | Codes |
|---|---|---|---|---|
| GET | `/api/message` | none | `message: string` | 200 |
| GET | `/api/time` | none | `utc_time: string` | 200 |
| POST | `/api/tasks` | JSON `{ "text": string }` | `task_id: UUID string`, `status: string` | 202, 400 |
| GET | `/api/tasks/{task_id}` | `task_id: UUID string` path | `task_id: string`, `status: queued/processing/completed/failed`, `result: string|null`, `error: string|null` | 200, 404 |

Errors: `{ "error": string }`. Empty body, arrays, numbers, missing `text`, blank text, text longer than 200 characters, and unknown fields are invalid. UUID paths with unknown IDs return 404. No authentication is provided in this educational implementation.

## Queue format and processing
One UTF-8 JSON message per file `data/queue/{task_id}.json`:
```json
{"task_id":"<uuid>","text":"example","created_at":"2026-10-26T00:00:00+00:00"}
```
Task state is stored in `data/tasks/{task_id}.json`. Worker atomically claims a queue file by moving it to `data/processing/`, writes `processing`, computes uppercase output, atomically saves `completed`, and removes the claimed message only **after** the result is stored. On worker startup, leftover claimed messages are returned to the queue. Filesystem atomic rename is assumed to work within the same volume. A worker crash after saving the result but before acknowledgment may replay a task; uppercase conversion is idempotent.

## Nonfunctional requirements and verification
- **N1:** Under normal local operation, `/api/message` returns within 500 ms for at least 95% of 100 sequential requests. Verify using `tests/check_latency.py`.
- **N2:** With one worker running, 10 short jobs finish within 15 seconds. Verify using `tests/test_api.py` integration test.
- **N3:** Invalid input and unknown task IDs always produce JSON errors without HTTP 500 in the test suite. Verify using `pytest`.

## Assumptions, design decisions, and risks
1. One local host and shared writable disk: file-based queue avoids AWS credentials; risk: it does not support separate hosts or network partitions.
2. Text tasks are small (max 200 characters): JSON files are simple and easy to inspect; risk: large workloads and high throughput are not supported.
3. Processing is idempotent: crash recovery may reprocess an unfinished job; risk: future non-idempotent work would require deduplication.
4. Only one worker is required for the demonstration; atomic claims support multiple workers, but concurrent load is not guaranteed.

## Environment
Python 3.10+, Flask, local writable `data/` directory. Run API and worker as separate processes. Not intended for production use: no authentication, rate limiting, distributed durability, or database transactions.
