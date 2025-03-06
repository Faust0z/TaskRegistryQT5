from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox

from utils.tasks_types import TaskTypes

class DeleteTaskType(QDialog):
    def __init__(self, parent=None, task_types: list[TaskTypes]=None):
        super().__init__(parent)
        self.tasks_types = task_types
        self.setWindowTitle("Delete a Task Type")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label_type_name = QLabel("Choose the Type to delete:")
        self.comBox_type_name = QComboBox(self)
        self.comBox_type_name.addItems(["Select..."])
        self.comBox_type_name.addItems(types.name for types in self.tasks_types)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.del_type_task)

        layout.addWidget(self.label_type_name)
        layout.addWidget(self.comBox_type_name)
        layout.addWidget(self.delete_button)

        self.return_type_name = None
        self.return_comBox_index = None

    def del_type_task(self):
        if not self.comBox_type_name.currentIndex() == 0:
            self.return_type_name = self.comBox_type_name.currentText()
            self.return_comBox_index = self.comBox_type_name.currentIndex()

        self.accept()