from fastapi import FastAPI, HTTPException, Path, Query, Response
from pydantic import BaseModel, Field

app = FastAPI(title="Task Tracker")

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120, pattern = r"\S")
    description: str = ""
    completed: bool = False

class TaskReplace(BaseModel):
    title: str = Field(min_length=1, max_length=120, pattern = r"\S")
    description: str 
    completed: bool

class TaskRead(TaskReplace):
    id: int


tasks: dict[int, dict] = {}
next_task_id = 1

def reset_tasks():
    global next_task_id
    next_task_id = 1
    tasks.clear()


def find_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code= 404, detail="Task not found")
    return tasks[task_id]


@app.post("/tasks", response_model= TaskRead, status_code=201)
def create_task(task: TaskCreate):
    global next_task_id
    saved = {"id": next_task_id, **task.model_dump()}
    tasks[next_task_id] = saved
    next_task_id += 1
    return saved
    

@app.get("/tasks", response_model= list[TaskRead], status_code=200)
def list_tasks(
    completed: bool | None = None,
):
    result = list(tasks.values())
    
    if completed is not None:
        result = [p for p in result if completed == p["completed"]]

    return result


@app.get("/tasks/{task_id}", response_model=TaskRead, status_code=200)
def get_task(task_id: int = Path(gt=0)):
    return find_task(task_id)


@app.put("/tasks/{task_id}", response_model=TaskRead, status_code=200)
def replace_task(task: TaskReplace, task_id: int = Path(gt=0)):
    find_task(task_id)
    saved = {"id": task_id, **task.model_dump()}
    tasks[task_id] = saved
    return saved

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id:int = Path(gt=0)):
    find_task(task_id)
    del tasks[task_id]
    return Response(status_code=204)