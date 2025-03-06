from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QPushButton
from PyQt5.uic import loadUi
from datetime import datetime as dt

from gui.dialogs.add_tasktype import AddTaskType
from gui.dialogs.delete_tasktype import DeleteTaskType
from utils.tasks import Tasks
from utils.tasks_types import TaskTypes
import utils.csv_manager as csv_manager

import copy


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        loadUi("gui/GUI.ui", self)
        self.done_tasks = csv_manager.read_done_tasks()
        self.tasks_types = csv_manager.read_tasks_types()
        self.set_ui()

    def set_ui(self):
        self.comBox_tasks_types.addItems(["Select..."])
        self.comBox_tasks_types.addItems(task.name for task in self.tasks_types)

        self.input_date.setDate(QDate.fromString(dt.today().strftime("%Y-%m-%d"), "yyyy-MM-dd"))
        self.input_date.setCalendarPopup(True)

        self.button_save.clicked.connect(self.save_task)
        self.button_add_type.clicked.connect(self.add_type_of_task)
        self.button_delete_type.clicked.connect(self.del_task_type)
        self.button_del_task.setEnabled(False)
        self.button_del_task.clicked.connect(self.del_task)

        self.load_tasks_into_table()
        self.done_tasks_table.itemSelectionChanged.connect(self.toggle_button_del_task)

    def save_task(self):
        task_type_name = self.comBox_tasks_types.currentText()
        task_type_id = next((types.id for types in self.tasks_types if types.name == task_type_name), None)
        greatest_id = int(self.done_tasks[-1].id) + 1 if self.done_tasks else 0
        elapsed_minutes = (dt.strptime(self.input_end_time.text(), "%H:%M") -
                           dt.strptime(self.input_start_time.text(), "%H:%M")).total_seconds() // 60
        new_task = Tasks(
            greatest_id,
            task_type_id,
            int(elapsed_minutes),
            self.input_date.text(),
            self.input_task_desc.toPlainText()
        )

        if self.validate_data(new_task):
            self.add_task_to_table(task_type_name, new_task.minutes_spent, new_task.date, new_task.description)
            QMessageBox.information(self, "Success", f"Task {task_type_name} saved with {new_task.minutes_spent} minutes")

            self.done_tasks.append(new_task)
            csv_manager.write_done_tasks(new_task)

            self.clear_inputs()

    def validate_data(self, new_task: Tasks) -> bool:
        errors = []
        if new_task.type_id is None:
            errors.append("Invalid task type selected.")
        if new_task.minutes_spent == 0:
            errors.append("Inserted time is 0.")
        if any(c in new_task.description for c in "\t\n\r"):
            errors.append("Description contains invalid characters (tabs or newlines).")

        if errors:
            QMessageBox.critical(self, "Error/s", "\n".join(errors))
            return False
        return True

    def clear_inputs(self):
        self.input_start_time.setTime(self.input_start_time.minimumTime())
        self.input_end_time.setTime(self.input_start_time.minimumTime())
        self.comBox_tasks_types.setCurrentIndex(0)
        self.input_date.setDate(QDate.fromString(dt.today().strftime("%Y-%m-%d"), "yyyy-MM-dd"))
        self.input_task_desc.clear()

    def del_task(self):
        selected_rows = set(index.row() for index in self.done_tasks_table.selectedIndexes())

        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText(f"Warning. Do you really want to delete the task?")
        msg.setIcon(QMessageBox.Warning)
        msg.addButton(QPushButton("Yes"), QMessageBox.YesRole)
        msg.addButton(QPushButton("Cancel"), QMessageBox.NoRole)
        msg.exec_()

        if selected_rows and msg.clickedButton().text() == "Yes":
            row_idx = selected_rows.pop()
            self.done_tasks_table.removeRow(row_idx)
            del self.done_tasks[row_idx]
            csv_manager.rewrite_done_tasks(self.done_tasks)

    def add_type_of_task(self):
        dialog = AddTaskType(self, self.tasks_types)

        if dialog.exec_():
            if self.type_already_exists(dialog.return_type_name):
                QMessageBox.critical(self, "Error", f"A task type named {dialog.return_type_name} already exists")
                return
            else:
                greatest_id = self.tasks_types[-1].id + 1
                new_task_type = TaskTypes(
                    greatest_id,
                    dialog.return_type_name,
                    dialog.return_type_desc
                )
                if csv_manager.write_task_type(new_task_type):
                    self.tasks_types.append(new_task_type)
                    self.comBox_tasks_types.addItem(dialog.return_type_name)

    def type_already_exists(self, name):
        return any(name == task.name for task in self.tasks_types)

    def del_task_type(self):
        dialog = DeleteTaskType(self, self.tasks_types)
        if dialog.exec_():
            type_id = self.search_selected_type_id(dialog.return_type_name)

            tasks_with_type = sum(task.type_id == type_id for task in self.done_tasks)
            if tasks_with_type > 0: # If there are any
                QMessageBox.warning(self, "Warning", f"Warning. Can't delete the type because {tasks_with_type} tasks use it")
                return
            else:
                task_type = next((t for t in self.tasks_types if t.name == dialog.return_type_name), None)
                if task_type: # If the task_type was found on the list (should always be True anyways)
                    self.comBox_tasks_types.removeItem(dialog.return_comBox_index)
                    self.tasks_types.remove(task_type)
                    csv_manager.rewrite_task_types(self.tasks_types)

    def search_selected_type_id(self, type_name) -> int:
        # This is necessary to do since the combobox only saves the NAME of the type, and not its id
        for types in self.tasks_types:  # Search for the index of the selected type
            if types.name == type_name:
                return types.id

    def load_tasks_into_table(self):
        self.done_tasks_table.setRowCount(len(self.done_tasks))

        done_tasks_copy = copy.deepcopy(self.done_tasks)
        for row_idx, task in enumerate(done_tasks_copy):
            for task_type in self.tasks_types: # Replace the id from the task with the task name from the tasks_types list
                if task.type_id == task_type.id:
                    task.type_id = task_type.name
                    break

            values = [task.type_id, str(task.minutes_spent), task.date, task.description]
            for col_idx, value in enumerate(values):
                self.done_tasks_table.setItem(row_idx, col_idx, QTableWidgetItem(value))

    def add_task_to_table(self, task_type,  time, date, desc):
        row_idx = self.done_tasks_table.rowCount()
        self.done_tasks_table.insertRow(row_idx)
        task_values = [task_type, str(time), date, desc]
        for col_idx, value in enumerate(task_values):
            self.done_tasks_table.setItem(row_idx, col_idx, QTableWidgetItem(value))

    def toggle_button_del_task(self):
        self.button_del_task.setEnabled(bool(self.done_tasks_table.selectedIndexes()))