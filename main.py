import copy
import sys
import csvmanager
from datetime import datetime as dt
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QPushButton
from dialogs import AddTaskType, DeleteTaskType
from PyQt5.uic import loadUi

from tasksmanagers import TasksManager, TypesManager

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        loadUi("GUI.ui", self)
        self.tasks_manager = TasksManager()
        self.types_manager = TypesManager()
        self.set_ui()

    def set_ui(self):
        self.comBox_tasks_types.addItems(["Select..."])
        self.comBox_tasks_types.addItems(task[1] for task in self.types_manager.tasks_types)

        self.input_date.setDate(QDate.fromString(dt.today().strftime("%Y-%m-%d"), "yyyy-MM-dd"))
        self.input_date.setCalendarPopup(True)

        self.button_save.clicked.connect(self.save_task)
        self.button_add_type.clicked.connect(self.add_type_of_task)
        self.button_delete_type.clicked.connect(self.del_type_of_task)
        self.button_del_task.setEnabled(False)
        self.button_del_task.clicked.connect(self.del_task)

        self.load_tasks_into_table()
        self.done_tasks_table.itemSelectionChanged.connect(self.toggle_button_del_task)

    def save_task(self):
        elapsed_minutes = (dt.strptime(self.input_end_time.text(), "%H:%M") -
                           dt.strptime(self.input_start_time.text(), "%H:%M")).total_seconds() // 60
        task_type_name = self.comBox_tasks_types.currentText()
        task_type_id = next((task[0] for task in self.types_manager.tasks_types if task[1] == task_type_name), None)
        desc = self.input_task_desc.toPlainText() or "No description"
        date = self.input_date.text()
        task_data = (task_type_id, elapsed_minutes, date, desc)

        if not self.validate_data(elapsed_minutes, task_type_id, desc): return

        if self.tasks_manager.add_task(task_data):
            self.add_task_to_table(task_type_name, elapsed_minutes, date, desc)
            QMessageBox.information(self, "Success", f"Task {task_type_name} saved with {elapsed_minutes} minutes")
            self.clear_inputs()

    def validate_data(self, elapsed_time, task_type_id, desc) -> bool:
        errors = []
        if task_type_id is None:
            errors.append("Invalid task type selected.")
        if elapsed_time == 0:
             errors.append("Inserted time is 0.")
        if any(c in desc for c in "\t\n\r"):
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
            del self.tasks_manager.done_tasks[row_idx]
            csvmanager.rewrite_csv_done_tasks(self.tasks_manager.done_tasks)

    def add_type_of_task(self):
        dialog = AddTaskType(self, self.types_manager.types_index, self.types_manager.tasks_types)
        if dialog.exec_() and dialog.return_type_name:
            if self.types_manager.add_task_type(dialog.return_type_name, dialog.return_type_desc):
                self.comBox_tasks_types.addItem(dialog.return_type_name)
            else:
                QMessageBox.critical(self, "Error", f"A task type named {dialog.return_type_name} already exists")

    def del_type_of_task(self):
        dialog = DeleteTaskType(self, self.types_manager.tasks_types)
        if dialog.exec_() and dialog.return_type_name:
            for task in self.types_manager.tasks_types: # Search for the index of the selected task
                if task[1] ==  dialog.return_type_name:
                    type_index = int(task[0])

            tasks_with_type = sum(task[1] == str(type_index) for task in self.tasks_manager.done_tasks)
            if tasks_with_type > 0: # If there are
                QMessageBox.warning(self, "Warning", f"Warning. Can't delete the type because {tasks_with_type} tasks use it")
                return

            if csvmanager.delete_task_type_by_index(str(type_index)):
                self.comBox_tasks_types.removeItem(dialog.return_comBox_index)

                for i, task in enumerate(self.types_manager.tasks_types):
                    if task[1] == dialog.return_type_name:
                        del self.types_manager.tasks_types[i]
                        break

    def load_tasks_into_table(self):
        self.done_tasks_table.setRowCount(len(self.tasks_manager.done_tasks))

        done_tasks_copy = copy.deepcopy(self.tasks_manager.done_tasks)
        for row_idx, task in enumerate(done_tasks_copy):
            for task_type in self.types_manager.tasks_types: # Replace the id from the task with the task name from the tasks_types list
                if task[1] == task_type[0]:
                    task[1] = task_type[1]
                    break
            for col_idx, value in enumerate(task[1:]): # Insert the values minus the index
                self.done_tasks_table.setItem(row_idx, col_idx, QTableWidgetItem(value))

    def add_task_to_table(self, task_type,  time, date, desc):
        row_idx = self.done_tasks_table.rowCount()
        self.done_tasks_table.insertRow(row_idx)
        task_values = [task_type, str(time), date, desc]
        for col_idx, value in enumerate(task_values):
            self.done_tasks_table.setItem(row_idx, col_idx, QTableWidgetItem(value))

    def toggle_button_del_task(self):
        self.button_del_task.setEnabled(bool(self.done_tasks_table.selectedIndexes()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = GUI()
    ventana.show()
    sys.exit(app.exec_())