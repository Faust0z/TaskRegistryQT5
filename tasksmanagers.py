import csvmanager

class TasksManager:
    def __init__(self):
        self.done_tasks = csvmanager.read_csv_done_tasks()
        self.tasks_index = int(self.done_tasks[-1][0]) if self.done_tasks else 0

    def add_task(self, task_data):
        self.tasks_index += 1
        task_data = (self.tasks_index, *task_data)  # Add new index
        if csvmanager.write_csv_done_tasks(task_data):
            self.done_tasks.append(task_data)
            return True
        return False

    def delete_task(self, task_index):
        self.done_tasks = [task for task in self.done_tasks if task[0] != task_index]
        return csvmanager.rewrite_csv_done_tasks(self.done_tasks)


class TypesManager:
    def __init__(self):
        self.tasks_types = csvmanager.read_csv_tasks_types()
        self.types_index = int(self.tasks_types[-1][0]) if self.tasks_types else 0

    def add_task_type(self, name, desc="No description") -> bool:
        if any(name == task[1] for task in self.tasks_types):
            return False  # Duplicate task type
        self.types_index += 1
        new_task_type = (self.types_index, name, desc)
        if csvmanager.write_csv_tasks_types(new_task_type):
            self.tasks_types.append(new_task_type)
            return True
        return False

    def delete_task_type(self, name) -> bool:
        type_index = next((task[0] for task in self.tasks_types if task[1] == name), None)
        if type_index is None:
            return False
        self.tasks_types = [task for task in self.tasks_types if task[0] != type_index]
        return csvmaganer.rewrite_csv_done_tasks(self.tasks_types)
