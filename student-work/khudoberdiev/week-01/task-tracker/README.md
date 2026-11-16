# Task Tracker API (Homework 03)

A FastAPI CRUD API for tasks, with in-memory storage.

## Install
From the repository root:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r student-work/khudoberdiev/week-01/task-tracker/requirements.txt
```

## Run the server
```bash
uvicorn main:app --app-dir student-work/khudoberdiev/week-01/task-tracker --reload
```
Open http://127.0.0.1:8000/docs

## Run the tests
```bash
cd student-work/khudoberdiev/week-01/task-tracker
python -m pytest -v
```

## Routes
| Route | Result |
|---|---|
| `POST /tasks` | 201 · 422 for an invalid body |
| `GET /tasks?completed=true/false` | 200 · 422 for an invalid boolean |
| `GET /tasks/{task_id}` | 200 · 404 · 422 |
| `PUT /tasks/{task_id}` | 200 · 404 · 422 (all fields required) |
| `DELETE /tasks/{task_id}` | 204 empty body · 404 · 422 |

## Example requests
- `POST /tasks` with `{"title": "Study FastAPI"}` → **201** `{"id": 1, "title": "Study FastAPI", "description": "", "completed": false}`
- `GET /tasks?completed=maybe` → **422** `bool_parsing`
- `PUT /tasks/2` with only `{"title": "x"}` → **422** `missing` description, completed
- `DELETE /tasks/1` → **204**, then `GET /tasks/1` → **404**

## Test results
```
collected 7 items

test_main.py::test_create_and_get_task PASSED        [ 14%]
test_main.py::test_filter_completed PASSED           [ 28%]
test_main.py::test_invalid_title_rejected PASSED     [ 42%]
test_main.py::test_missing_and_invalid_id PASSED     [ 57%]
test_main.py::test_replace_task PASSED               [ 71%]
test_main.py::test_delete_task PASSED                [ 85%]
test_main.py::test_ids_not_reused PASSED             [100%]

7 passed, 1 warning in 0.24s
```
The one warning comes from FastAPI's test client library (an `httpx` deprecation notice), not from this code.

## In-memory limitation
Tasks are stored in a Python dictionary (`tasks`) in the server's memory. When the server restarts or reloads, the code runs again from the top: `tasks` becomes an empty `{}` and `next_task_id` goes back to 1. All saved tasks are lost. A database would keep them across restarts.

## A bug I investigated
In the DELETE test I first checked `response.json() == b""`. A 204 response has an empty body, and an empty body isn't valid JSON, so `.json()` would crash with a `JSONDecodeError`. I switched to `response.content`, which returns the raw bytes, and checked `response.content == b""`. This was caught during code review, before I ran the tests.


## AI assistance
I used Claude for pseudocode hints, explanations, and reviewing my code. I wrote the code myself, and verified every route by hand in `/docs` and with 7 pytest tests.