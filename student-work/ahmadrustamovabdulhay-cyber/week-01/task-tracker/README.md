# Task Tracker API

A simple REST API built with **Python** and **FastAPI** that allows users to manage tasks. The API supports creating, retrieving, updating, and deleting tasks, as well as filtering tasks by their completion status.

## Features

- Create new tasks
- Retrieve all tasks
- Retrieve a specific task by its ID
- Update existing tasks
- Delete tasks
- Filter tasks by completion status (`true` or `false`)
- Validate task titles and descriptions using Pydantic
- Handle invalid input and missing tasks with appropriate HTTP errors
- Automatically assign unique, incrementing task IDs during runtime

## Technologies Used

- **Python** – Programming language
- **FastAPI** – Web framework for building the REST API
- **Pydantic** – Data validation and serialization
- **Uvicorn** – ASGI server
- **Pytest** – Automated testing framework

## Project Structure

```text
task-tracker/
│
├── main.py
├── models.py
├── requirements.txt
├── README.md
│
└── tests/
    └── test_tasks.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ahmadrustamovabdulhay-cyber/ai-engineering-course.git
```

### 2. Navigate to the project directory

```bash
cd ai-engineering-course/student-work/ahmadrustamovabdulhay-cyber/week-01/task-tracker
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks?completed=true` | Filter completed tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update an existing task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Running Tests

Run the automated test suite from the project directory:

```bash
pytest -v
```

The tests cover API functionality, input validation, error handling, task filtering, and task creation, updating, and deletion.

## Notes

- Tasks are stored in an in-memory Python dictionary.
- Task data is not persistent and will be reset when the application restarts.
- Task IDs increment during the application's runtime.


## Notes and Limitations

- Tasks are stored in an in-memory Python dictionary.
- Task data is not persistent and will be reset when the application restarts: the list returns to the two sample tasks.
- Task IDs increment during the application's runtime and start again after 2 on restart, so they are unique only within one process lifetime.

## Bug Investigated
One issue occurred when generating task IDs using the maximum existing ID plus one.

After deleting a task, this approach could reuse an ID that had already been assigned.

I fixed this by introducing an incrementing ID counter that continues increasing during the application's runtime.

The behavior is covered by test_delete_and_create_task: it deletes a task, creates a new one, and checks that the remaining tasks are unchanged and the new ID is higher than any previous ID.

## AI Assistance

AI assistance was used to understand implementation concepts,
investigate bugs, improve automated tests, and review project
documentation.

All suggested changes were reviewed, tested, and verified
using pytest and manual API requests.



