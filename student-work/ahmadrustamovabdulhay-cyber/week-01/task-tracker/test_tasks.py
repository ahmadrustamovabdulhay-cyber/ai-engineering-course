

from fastapi.testclient import TestClient
import pytest
import main

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def reset_tasks():
    main.next_id = 3
    main.tasks.clear()
    main.tasks.update({
        1: {"id": 1,
            "title": "Learn FastAPI",
            "description": "Read the FastAPI documentation and build a sample project.",
            "completed": False},
        2: {"id": 2,
            "title": "Write Unit Tests",
            "description": "Write unit tests for the FastAPI application using pytest.",    
            "completed": False}
    })

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    expected_id = max([task["id"] for task in client.get("/tasks").json()]) + 1
    response = client.post(
        "/tasks",
        json = {"title": "Test the code",
                "description": "Write tests for the code",
                "completed": False
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == expected_id
    assert data["title"] == "Test the code"
    assert data["description"] == "Write tests for the code"
    assert data["completed"] is False

def test_get_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Read the FastAPI documentation and build a sample project."
    assert data["completed"] is False
def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
def test_get_task_invalid_id():
    response = client.get("/tasks/abc")
    assert response.status_code == 422
    data = response.json()

   

def test_filter_tasks():
    response = client.get("/tasks?completed=false")
    assert response.status_code == 200
    data = response.json()
    assert all(task["completed"] is False for task in data)

    response = client.get("/tasks?completed=true")
    assert response.status_code == 200
    data = response.json()
    assert all(task["completed"] is True for task in data)

def test_task_empty_title():
    before = client.get("/tasks").json()
    response = client.post(
        "/tasks",
        json={"title": " ",
              "description": "This is a test task",
              "completed": False}
    )
    after = client.get("/tasks").json()
    assert response.status_code == 422
    data = response.json()
    assert before == after

def test_task_missing_title():
    before = client.get("/tasks").json()
    response = client.post(
        "/tasks",
        json={"description": "This is a test task",
              "completed": False}
    )
    after = client.get("/tasks").json()
    assert response.status_code == 422
    data = response.json()
    assert before == after

def test_task_long_title():
    before = client.get("/tasks").json()
    long_title = "A" * 121
    response = client.post(
        "/tasks",
        json={"title": long_title,
              "description": "This is a test task",
              "completed": False}
    )
    after = client.get("/tasks").json()
    assert response.status_code == 422
    data = response.json()
    assert before == after

def test_update_task():
    response = client.put(
        "/tasks/1",
        json={"title": "Updated Task",
              "description": "This task has been updated",
              "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Updated Task"
    assert data["description"] == "This task has been updated"
    assert data["completed"] is True
def test_update_task_invalid_title():
    before = client.get("/tasks").json()
    response = client.put(
        "/tasks/1",
        json={
              "description": "This task has been updated",
              "completed": True}
    )
    after = client.get("/tasks").json()
    assert response.status_code == 422
    data = response.json()
    assert before == after

def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    get_response = client.get("/tasks/1")
    assert get_response.status_code == 404
    delete_response = client.delete("/tasks/1")
    assert delete_response.status_code == 404
def test_delete_and_create_task():
    task_before = client.get("/tasks").json()
    response = client.delete("/tasks/2")
    assert response.status_code == 204
    create_response = client.post(
        "/tasks",
        json={"title": "New Task",
              "description": "This is a new task",
              "completed": False}
    )
    assert create_response.status_code == 201
    task_after = client.get("/tasks").json()
    assert len(task_after) == len(task_before)
    assert all(task in task_after for task in task_before if task["id"] != 2)
    assert max(task["id"] for task in task_after) == max(task["id"] for task in task_before) + 1
    data = create_response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "This is a new task"
    assert data["completed"] is False
