from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel, Field, field_validator



class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    completed: bool = Field(default=False)

    @field_validator("title")
    def title_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Title must not be empty")
        return value

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool

app = FastAPI(title="Task Tracker API")

tasks = {
    1:{"id": 1,
       "title": "Learn FastAPI",
       "description": "Read the FastAPI documentation and build a sample project.",
       "completed": False},

    2:{"id": 2,
       "title": "Write Unit Tests",
        "description": "Write unit tests for the FastAPI application using pytest.",
         "completed": False},
}
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(completed: bool | None = Query(default=None,
               description="Filter tasks by completion status")):
    if completed is None:
        return list(tasks.values())
    return [task for task in tasks.values() if task["completed"] == completed]
@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int = Path(gt=0)):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
@app.post("/tasks", status_code=201, response_model=TaskRead)
def create_task(task: TaskCreate):
    global next_id
    new_id = next_id

    new_task = task.model_dump()
    new_task["id"] = new_id

    tasks[new_id] = new_task
    next_id += 1

    return new_task

@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int = Path(gt=0), task: TaskCreate = Body(...)):
    existing_task = tasks.get(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = task.model_dump()
    updated_task["id"] = task_id

    tasks[task_id] = updated_task

    return updated_task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int = Path(gt=0)):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return None
