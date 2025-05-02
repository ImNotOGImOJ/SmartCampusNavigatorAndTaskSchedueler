import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Campus Navigator")
        self.setGeometry(300, 200, 500, 400)
        
        # Create label for the title
        title_label = QLabel("Smart Campus Navigator", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        
        # Create buttons for navigation
        campus_nav_button = QPushButton("Campus Navigation", self)
        task_scheduler_button = QPushButton("Task Scheduler", self)
        exit_button = QPushButton("Exit", self)
        
        # Style buttons
        button_style = "font-size: 18px; padding: 15px; margin: 10px;"
        campus_nav_button.setStyleSheet(button_style)
        task_scheduler_button.setStyleSheet(button_style)
        exit_button.setStyleSheet(button_style)
        
        # Connect buttons to functions
        campus_nav_button.clicked.connect(self.open_campus_navigation)
        task_scheduler_button.clicked.connect(self.open_task_scheduler)
        exit_button.clicked.connect(self.close)
        
        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(campus_nav_button)
        layout.addWidget(task_scheduler_button)
        layout.addWidget(exit_button)
        
        self.setLayout(layout)
    
    def open_campus_navigation(self):
        from campus_navigation import CampusNavigation  # Import here to avoid circular import
        self.campus_nav_window = CampusNavigation()
        self.campus_nav_window.show()
        self.close()

    def open_task_scheduler(self):
        from task_scheduler import TaskScheduler  # Import here to avoid circular import
        self.task_scheduler_window = TaskScheduler()
        self.task_scheduler_window.show()
        self.close()