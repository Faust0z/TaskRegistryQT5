from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QPlainTextEdit


class AddTaskType(QDialog):
    def __init__(self, parent=None, types_index=0, tasks_types=None):
        super().__init__(parent)
        self.types_index = types_index
        self.tasks_types = tasks_types
        self.setWindowTitle("Add a new Task Type")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label_type_name = QLabel("Type name:")
        self.input_type_name = QLineEdit(self)
        self.label_type_desc = QLabel("Type description (optional):")
        self.input_type_desc = QPlainTextEdit(self)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_type_task)

        layout.addWidget(self.label_type_name)
        layout.addWidget(self.input_type_name)
        layout.addWidget(self.label_type_desc)
        layout.addWidget(self.input_type_desc)
        layout.addWidget(self.add_button)

        self.return_type_name = None
        self.return_type_desc = None

    def add_type_task(self):
        name = self.input_type_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Task name cannot be empty.")
        else:
            self.return_type_name = name
            self.return_type_desc = self.input_type_desc.toPlainText().strip() or "No description"

        self.accept()


class DeleteTaskType(QDialog):
    def __init__(self, parent=None, tasks_types: list=None):
        super().__init__(parent)
        self.tasks_types = tasks_types
        self.setWindowTitle("Delete a Task Type")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label_type_name = QLabel("Choose the Type to delete:")
        self.comBox_type_name = QComboBox(self)
        self.comBox_type_name.addItems(["Select..."])
        self.comBox_type_name.addItems(task[1] for task in self.tasks_types)

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