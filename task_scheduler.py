import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QComboBox, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QLabel, QTimeEdit, QScrollArea,
                            QTableWidget, QTableWidgetItem, QHeaderView, QGridLayout)
from PyQt5.QtCore import Qt, QTime

class Task:
    def __init__(self, name, priority, start_time, end_time):
        self.name = name
        self.priority = priority  
        self.start_time = start_time
        self.end_time = end_time
        
    def get_duration(self):
        # Convert times to minutes since midnight for calculation
        start_minutes = self.start_time.hour() * 60 + self.start_time.minute()
        end_minutes = self.end_time.hour() * 60 + self.end_time.minute()
        return end_minutes - start_minutes
    
    def get_priority_value(self):
        if self.priority == "High":
            return 3
        elif self.priority == "Medium":
            return 2
        else:  # Low
            return 1

class TaskScheduler(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Scheduler")
        self.setGeometry(300, 100, 750, 600)
        
        # List to store tasks
        self.tasks = []

        # Create label for the title
        title_label = QLabel("Task Scheduler", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Create input fields
        self.task_name_input = QLineEdit(self)
        self.task_name_input.setPlaceholderText("Enter task name")
        
        self.start_time_input = QTimeEdit(self)
        self.end_time_input = QTimeEdit(self)

        # Set default time format
        self.start_time_input.setDisplayFormat("HH:mm")
        self.end_time_input.setDisplayFormat("HH:mm")

        self.priority_dropdown = QComboBox(self)
        self.priority_dropdown.addItems(["Low", "Medium", "High"])

        # Create buttons
        self.add_task_button = QPushButton("Add Task", self)
        self.add_task_button.clicked.connect(self.add_task)
        
        self.remove_task_button = QPushButton("Remove Selected Task", self)
        self.remove_task_button.clicked.connect(self.remove_task)
        
        self.optimize_schedule_button = QPushButton("Optimize Schedule", self)
        self.optimize_schedule_button.clicked.connect(self.optimize_schedule)
        
        # Back button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.go_back)

        # Set button styles
        button_style = "font-size: 16px; padding: 8px; margin: 5px;"
        self.add_task_button.setStyleSheet(button_style)
        self.remove_task_button.setStyleSheet(button_style)
        self.optimize_schedule_button.setStyleSheet(button_style)
        back_button.setStyleSheet(button_style)

        # Create task table
        self.task_table = QTableWidget(0, 4)
        self.task_table.setHorizontalHeaderLabels(["Task Name", "Priority", "Start Time", "End Time"])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_table.setMinimumHeight(200)

        # Create layout
        layout = QVBoxLayout()

        # Task Input Layout (Task Name, Priority, Start/End Time)
        input_layout = QGridLayout()
        input_layout.addWidget(QLabel("Task Name:"), 0, 0)
        input_layout.addWidget(self.task_name_input, 0, 1)
        input_layout.addWidget(QLabel("Priority:"), 0, 2)
        input_layout.addWidget(self.priority_dropdown, 0, 3)
        input_layout.addWidget(QLabel("Start Time:"), 1, 0)
        input_layout.addWidget(self.start_time_input, 1, 1)
        input_layout.addWidget(QLabel("End Time:"), 1, 2)
        input_layout.addWidget(self.end_time_input, 1, 3)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_task_button)
        button_layout.addWidget(self.remove_task_button)
        button_layout.addWidget(self.optimize_schedule_button)

        layout.addWidget(title_label)
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("Current Tasks:"))
        layout.addWidget(self.task_table)
        
        # Results area for the optimized schedule
        self.schedule_results = QLabel("Optimized Schedule will appear here")
        layout.addWidget(self.schedule_results)
        layout.addWidget(back_button)

        self.setLayout(layout)
        
    def add_task(self):
        task_name = self.task_name_input.text().strip()
        if not task_name:
            return  # Don't add empty tasks
            
        priority = self.priority_dropdown.currentText()
        start_time = self.start_time_input.time()
        end_time = self.end_time_input.time()
        
        # Validate times
        if start_time >= end_time:
            self.schedule_results.setText("Error: End time must be after start time")
            return
            
        # Create task and add to list
        new_task = Task(task_name, priority, start_time, end_time)
        self.tasks.append(new_task)
        
        # Add to table
        row_position = self.task_table.rowCount()
        self.task_table.insertRow(row_position)
        
        self.task_table.setItem(row_position, 0, QTableWidgetItem(task_name))
        self.task_table.setItem(row_position, 1, QTableWidgetItem(priority))
        self.task_table.setItem(row_position, 2, QTableWidgetItem(start_time.toString("HH:mm")))
        self.task_table.setItem(row_position, 3, QTableWidgetItem(end_time.toString("HH:mm")))
        
        # Clear inputs
        self.task_name_input.clear()

    def remove_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            self.task_table.removeRow(selected_row)
            self.tasks.pop(selected_row)
            
    def sorting_activity(self, activities):
        # Step 1: Sort tasks by end time (greedy approach)
        activities.sort(key=lambda x: x.end_time)  # Sort by end time

        # Step 2: Initialize the selected activities list with the first task
        selected_activities = [activities[0]]
        last_selected = activities[0]

        # Step 3: Iterate through the remaining activities
        for i in range(1, len(activities)):
            # Step 4: Check if the start time of the current activity is after the last selected task's end time
            if activities[i].start_time >= last_selected.end_time:
                selected_activities.append(activities[i])
                last_selected = activities[i]

        return selected_activities

    def optimize_schedule(self):
        if not self.tasks:
            self.schedule_results.setText("No tasks to optimize")
            return
        
        # Step 1: Sort tasks by priority (highest first)
        sorted_tasks = sorted(self.tasks, key=lambda t: t.get_priority_value(), reverse=True)

        # Step 2: Use the greedy algorithm to get the non-overlapping tasks
        selected_tasks = self.sorting_activity(sorted_tasks)

        # Step 3: Display optimized schedule
        schedule_text = "Optimized Schedule:\n\n"
        for i, task in enumerate(selected_tasks):
            schedule_text += f"{i+1}. {task.name} ({task.priority})\n"
            schedule_text += f"   Time: {task.start_time.toString('HH:mm')} - {task.end_time.toString('HH:mm')}\n"
            schedule_text += f"   Duration: {task.get_duration()} minutes\n\n"

        self.schedule_results.setText(schedule_text)
        
    def go_back(self):
        from main_menu import MainPage  # Import here to avoid circular import
        self.main_menu = MainPage()
        self.main_menu.show()
        self.close()  # Close the current window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskScheduler()
    window.show()
    sys.exit(app.exec_())
