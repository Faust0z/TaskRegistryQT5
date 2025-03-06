from utils.tasks import Tasks
from utils.tasks_types import TaskTypes

import pandas as pd
import os.path

types_route = os.path.join(os.path.dirname(__file__), "..", "data", "tasks_types.csv")
os.makedirs(os.path.dirname(types_route), exist_ok=True)
tasks_route = os.path.join(os.path.dirname(__file__), "..", "data", "done_tasks.csv")
os.makedirs(os.path.dirname(tasks_route), exist_ok=True)

def read_tasks_types() -> list[TaskTypes]:
    if not os.path.exists(types_route):
        df = pd.DataFrame(columns=["id", "name", "description"])
        df.to_csv(types_route, index=False, encoding="utf-8")
        return []

    task_types = []
    df = pd.read_csv(types_route)
    for _, row in df.iterrows():
        task_types.append(TaskTypes(row["id"], row["name"], row["description"]))
    return task_types

def write_task_type(type_data: TaskTypes) -> bool:
    try:
        df = pd.DataFrame([vars(type_data)], columns=["id", "name", "description"])
        df.to_csv(types_route, mode="a", header=False, index=False)
        return True
    except (IOError, OSError, ValueError) as e:
        print(f"Error writing CSV: {e}")
        return False

def rewrite_task_types(task_types: list[TaskTypes]) -> bool:
    try: # It's easier to just dump the list into the csv than delete a line
        types_data = [{
            'id': types.id,
            'name': types.name,
            'description': types.description
        } for types in task_types]

        df = pd.DataFrame(types_data, columns=["id", "name", "description"])
        df.to_csv(types_route, index=False, header=True, encoding="utf-8")
        return True
    except (IOError, OSError, ValueError) as e:
        print(f"Error writing tasks: {e}")
        return False

def read_done_tasks() -> list[Tasks]:
    if not os.path.exists(tasks_route):
        df = pd.DataFrame(columns=["id", "type_id", "minutes_spent", "date", "description"])
        df.to_csv(tasks_route, index=False, encoding="utf-8")
        return []

    done_tasks = []
    df = pd.read_csv(tasks_route)
    for _, row in df.iterrows():
        done_tasks.append(Tasks(row["id"], row["type_id"], row["minutes_spent"], row["date"], row["description"]))
    return done_tasks

def write_done_tasks(task_data: Tasks) -> bool:
    try:
        df = pd.DataFrame([vars(task_data)], columns=["id", "type_id", "minutes_spent", "date", "description"])
        df.to_csv(tasks_route, mode="a", header=False, index=False)
        return True
    except (IOError, OSError, ValueError) as e:
        print(f"Error writing CSV: {e}")
        return False

def rewrite_done_tasks(done_tasks: list[Tasks]):
    try: # It's easier to just dump the list into the csv than delete a line
        tasks_data = [{
            'id': task.id,
            'type_id': task.type_id,
            'minutes_spent': task.minutes_spent,
            'date': task.date,
            'description': task.description
        } for task in done_tasks]

        df = pd.DataFrame(tasks_data, columns=["id", "type_id", "minutes_spent", "date", "description"])
        df.to_csv(tasks_route, index=False, header=True, encoding="utf-8")
        return True
    except (IOError, OSError, ValueError) as e:
        print(f"Error writing tasks: {e}")
        return False