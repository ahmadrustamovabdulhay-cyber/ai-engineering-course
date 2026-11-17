import pytest
from fastapi.testclient import TestClient
import task_tracker

@pytest.fixture
def client():
    task_tracker.reset_tasks()
    with TestClient(task_tracker.app) as test_client:
        yield test_client
    task_tracker.reset_tasks()



def test_create_and_retreive_task(client):
    payload = {"title": "Gym"}
    response = client.post("/tasks", json = payload)
    assert response.status_code == 201
    saved = response.json()
    assert saved["title"] == "Gym"
    assert saved["description"] == ""
    assert saved["completed"] == False
    assert client.get(f"/tasks/{saved["id"]}").json() == saved



def test_completed_filter(client):
    payload_1 = {"title": "Playing chess", "completed": True}
    task_1 = client.post("/tasks", json = payload_1).json()
    assert client.get("/tasks", params = {"completed": True}).json() == [task_1]
    assert client.get("/tasks", params = {"completed": False}).json() == []
    assert client.get("/tasks").json() == [task_1] 

    payload_2 = {"title": "Coding", "completed": False}
    task_2 = client.post("/tasks", json = payload_2).json()
    assert client.get("/tasks", params = {"completed": True}).json() == [task_1]
    assert client.get("/tasks", params = {"completed": False}).json() == [task_2]
    assert client.get("/tasks").json() == [task_1, task_2]



@pytest.mark.parametrize("changes",[
    {"title": ""}, {"title": "    "}, {"title": "x" * 121},
])
def test_invalid_title_creation(client, changes):
    payload = {**changes}
    response =  client.post("/tasks", json = payload)
    assert response.status_code == 422
    assert client.get("/tasks").json() == []



@pytest.mark.parametrize("changes",[
    {"title": ""}, {"title": "    "}, {"title": "x" * 121},
])
def test_invalid_title_replacement(client, changes):
    payload_1 = {"title": "Playing chess", "completed": True}
    task_1 = client.post("/tasks", json = payload_1).json()
    payload = {"description": "", "completed": False, **changes, "id": 1}
    response = client.put("/tasks/1", json = payload)
    assert response.status_code == 422 
    assert client.get("/tasks").json() == [task_1]



def test_find_missing_task_invalid_path(client):
    payload_1 = {"title": "Playing chess"}
    task_1 = client.post("/tasks", json = payload_1).json()
    assert client.get("/tasks/0").status_code == 422
    assert client.get("/tasks/abc").status_code == 422
    assert client.get("/tasks/999").status_code == 404
    assert client.get(f"/tasks/{task_tracker.next_task_id}").status_code == 404
    assert client.get("/tasks_list").status_code == 404



def test_replacement_and_incomplete_replacement(client):
    task_1 = {"title": "Playing chess"}
    before = client.post("/tasks", json = task_1).json()
    incomplete = {"title": "Reading a book", "description": "Atomic Habits"}
    assert client.put("/tasks/1", json = incomplete).status_code == 422
    assert client.get("/tasks/1").json() == before
    complete = {**incomplete, "completed": True}
    response = client.put("/tasks/1", json = complete)
    assert response.status_code == 200
    assert response.json() == {**complete, "id": 1}
    assert client.put("/tasks/999", json = complete).status_code == 404



def test_delete_task_and_check_id(client):
    payload_1 = {"title": "Playing chess"}
    task_1 = client.post("/tasks", json = payload_1).json()
    payload_2 = {"title": "Coding", "completed": False}
    task_2 = client.post("/tasks", json = payload_2).json()
    response = client.delete("/tasks/2")
    assert response.status_code == 204
    assert client.get("/tasks/2").status_code == 404
    assert client.delete("/tasks/2").status_code == 404
     
    payload_3 = {"title": "Reading a book"}
    task_3 = client.post("/tasks", json = payload_3).json()
    assert task_3["id"] != 2
