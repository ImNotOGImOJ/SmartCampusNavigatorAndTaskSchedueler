import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QLineEdit, QPushButton, QGraphicsView, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class CampusNavigator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campus Navigator")
        self.setGeometry(100, 100, 1000, 600)

        # Main layout: horizontal
        main_layout = QHBoxLayout()

        # Left Panel
        left_panel = QVBoxLayout()

        # Title
        title = QLabel("Campus Navigator")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)

        # Input Box
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter your tasks/classes here...")


        #ADD FUNCTIONS WHEN READY
        # Start Button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.run_program)

        # Output Box
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Your ordered tasks will appear here...")

        # Add widgets to left panel
        left_panel.addWidget(title)
        left_panel.addWidget(self.input_box)
        left_panel.addWidget(self.start_button)
        left_panel.addWidget(self.output_box)

        # Right Panel - Placeholder for Map
        map_view = QGraphicsView()
        map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add panels to main layout
        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(map_view, 2)

        self.setLayout(main_layout)

    def run_program(self):
        input_text = self.input_box.text()
        if input_text:
            tasks = [task.strip() for task in input_text.split(",")]
            ordered_tasks = "\n".join(f"{i+1}. {task}" for i, task in enumerate(tasks))
            self.output_box.setText(ordered_tasks)
        else:
            self.output_box.setText("Please enter some tasks or classes.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CampusNavigator()
    window.show()
    sys.exit(app.exec_())