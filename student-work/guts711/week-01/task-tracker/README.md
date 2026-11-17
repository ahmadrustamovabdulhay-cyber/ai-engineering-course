# A Task Tracker App

## Installing Dependencies
bash:
python -m venv .venv
source .venv/Scripts/activate  
pip install -r requirements.txt


## Starting the server
uvicorn task_tracker:app --reload --app-dir ./student-work/guts711/week-01/task-tracker

## Runnning pytest
cd ./student-work/guts711/week-01/task-tracker
pytest -vv test.py


## The in-memory limitation and one bug you investigated
Because there is no permanent database resting the server triggers for all tasks(data) to be removed 


