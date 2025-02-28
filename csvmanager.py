import csv
import os.path

types_route = "data/tasks_types.csv"
tasks_route = "data/done_tasks.csv"

def read_csv_tasks_types() -> list:
    if not os.path.exists(types_route):
        open(types_route, "w", newline="", encoding="utf-8")
        return []

    tasks_types = []
    with open(types_route, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            tasks_types.append(row)
    return tasks_types

def read_csv_done_tasks() -> list:
    if not os.path.exists(tasks_route):
        open(tasks_route, "w", newline="", encoding="utf-8")
        return []

    done_tasks = []
    with open(tasks_route, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            done_tasks.append(row)
    return done_tasks

def write_csv_done_tasks(task_data: tuple) -> bool:
    try:
        with open(tasks_route, mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(task_data)
        return True
    except (IOError, OSError, csv.Error) as e:
        print(f"Error writing CSV: {e}")
        return False

def write_csv_tasks_types(type_data: tuple) -> bool:
    try:
        with open(types_route, mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(type_data)
        return True
    except (IOError, OSError, csv.Error) as e:
        print(f"Error writing CSV: {e}")
        return False

def delete_task_type_by_index(index_value: str) -> bool:
    try:
        with open(types_route, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader if row[0] != index_value]

        with open(types_route, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
        return True
    except (IOError, OSError, csv.Error, IndexError) as e:
        print(f"Error deleting task type: {e}")
        return False

def rewrite_csv_done_tasks(done_tasks: list):
    try: # It's easier to just dump the done_tasks list into the csv than delete a particular task
        with open(tasks_route, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(done_tasks)
        return True
    except (IOError, OSError, csv.Error, IndexError) as e:
        print(f"Error deleting task type: {e}")
        return False