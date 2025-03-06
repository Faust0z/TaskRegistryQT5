from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QPlainTextEdit

class AddTaskType(QDialog):
    def __init__(self, parent=None, tasks_types=None):
        super().__init__(parent)
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
            return
        else:
            self.return_type_name = name
            self.return_type_desc = self.input_type_desc.toPlainText().strip() or "No description"

        self.accept()