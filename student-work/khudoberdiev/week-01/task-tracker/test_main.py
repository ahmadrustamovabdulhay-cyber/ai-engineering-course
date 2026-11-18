import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client():
    main.reset_store()
    with TestClient(main.app) as test_client:
        yield test_client
    main.reset_store()

# test 1: creating a task and reading it back works correctly
def test_create_and_get_task(client):
    response = client.post("/tasks", json={"title": "Study"})   # send POST with a body
    assert response.status_code == 201                          # created?

    saved = response.json()                                     # body → Python dict
    assert saved["id"] == 1                                     # server made the ID
    assert saved["description"] == ""                           # default used
    assert saved["completed"] is False                          # default used

    got = client.get(f"/tasks/{saved['id']}")                   # read it back
    assert got.status_code == 200
    assert got.json() == saved                                  # same task stored


# test 2: filtering by completed returns the right tasks, including false and no matches
def test_filter_completed(client):
    client.post("/tasks", json = {"title" : "Done", "completed":True})
    client.post("/tasks", json = {"title": "Todo"})

    got_true = client.get(f"/tasks?completed=true")
    assert got_true.status_code == 200
    ids = [t["id"] for t in got_true.json()]
    assert ids == [1]

    got_false = client.get(f"/tasks?completed=false")
    ids = [f["id"] for f in got_false.json()]
    assert ids == [2]

    got = client.get(f"/tasks")
    ids = [g["id"] for g in got.json()]
    assert ids == [1,2]

    client.delete("/tasks/1")

    got_none = client.get("/tasks?completed=true")
    assert got_none.status_code == 200
    assert got_none.json() == []

# test 3: missing, empty, or too-long titles are rejected and nothing is saved
def test_invalid_title_rejected(client):
    for body in [{}, {"title": ""}, {"title": "x" * 121}]:
        response = client.post("/tasks", json = body)
        assert response.status_code == 422

    assert client.get("/tasks").json() == []


# test 4: a missing task gives 404, an invalid ID gives 422
def test_missing_and_invalid_id(client):
    assert client.get("/tasks/999").status_code == 404
    assert client.get("/tasks/abc").status_code == 422
    assert client.get("/tasks/0").status_code == 422


# test 5: PUT replaces all fields and keeps the ID; an incomplete body changes nothing
def test_replace_task(client):
    client.post("/tasks", json = {"title": "Old"})
    before = client.get("/tasks/1").json()

    assert client.put("/tasks/1", json = {"title": "x"}).status_code == 422
    assert client.get("/tasks/1").json() == before

    full = {"title": "New", "description": "updated", "completed": True}
    response = client.put("/tasks/1", json = full)
    assert response.status_code == 200
    assert response.json() == {"id":1, **full}

# test 6: DELETE returns an empty 204; getting or deleting again gives 404
def test_delete_task(client):
    client.post("/tasks", json  = {"title":"for deletion"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    assert response.content == b""

    got_none = client.get("/tasks/1")
    assert got_none.status_code == 404
    response_again = client.delete("/tasks/1")
    assert response_again.status_code == 404


# test 7: after a delete, a new task gets a new ID and existing tasks stay intact
def test_ids_not_reused(client):
    client.post("/tasks", json={"title": "First"})    # gets id 1
    client.post("/tasks", json={"title": "Second"})   # gets id 2

    client.delete("/tasks/1")
    response = client.post("/tasks", json={"title": "Third"})   
    assert response.json()["id"] == 3
    all_tasks = client.get("/tasks").json()
    ids = [t["id"] for t in all_tasks]
    assert ids == [2, 3]

