import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QTextEdit, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt

class CampusNavigation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campus Navigation")
        self.setGeometry(300, 100, 600, 500)
        
        # Create label for the title
        title_label = QLabel("Campus Navigation", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 15px;")
        
        # Location selection
        location_group = QGroupBox("Location")
        location_layout = QGridLayout()
        
        # Starting point
        start_label = QLabel("Start Location:")
        self.start_combo = QComboBox()
        self.start_combo.addItems(["Library", "Student Center", "Engineering Building", 
                                  "Science Building", "Cafeteria", "Dormitory", "Parking Lot"])
        
        # Destination point
        dest_label = QLabel("Destination:")
        self.dest_combo = QComboBox()
        self.dest_combo.addItems(["Library", "Student Center", "Engineering Building", 
                                 "Science Building", "Cafeteria", "Dormitory", "Parking Lot"])
        
        # Add to grid layout
        location_layout.addWidget(start_label, 0, 0)
        location_layout.addWidget(self.start_combo, 0, 1)
        location_layout.addWidget(dest_label, 1, 0)
        location_layout.addWidget(self.dest_combo, 1, 1)
        location_group.setLayout(location_layout)
        
        # Navigation options
        options_group = QGroupBox("Navigation Options")
        options_layout = QVBoxLayout()
        
        self.shortest_path_button = QPushButton("Find Shortest Path")
        self.shortest_path_button.clicked.connect(self.find_shortest_path)
        
        self.fastest_path_button = QPushButton("Find Fastest Path")
        self.fastest_path_button.clicked.connect(self.find_fastest_path)
        
        options_layout.addWidget(self.shortest_path_button)
        options_layout.addWidget(self.fastest_path_button)
        options_group.setLayout(options_layout)
        
        # Results area
        self.result_label = QLabel("Navigation Results:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(150)
        
        # Back button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.go_back)
        
        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(location_group)
        layout.addWidget(options_group)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)
        layout.addWidget(back_button)
        
        self.setLayout(layout)
    
    def find_shortest_path(self):
        start = self.start_combo.currentText()
        dest = self.dest_combo.currentText()
        
        # This is where you would implement your graph algorithm
        # For now, showing a placeholder result
        result = f"Shortest path from {start} to {dest}:\n\n"
        result += f"{start} → Center Plaza → North Walkway → {dest}\n"
        result += f"Distance: 0.7 miles"
        
        self.result_text.setText(result)
        
    def find_fastest_path(self):
        start = self.start_combo.currentText()
        dest = self.dest_combo.currentText()
        
        # This is where you would implement your graph algorithm
        # For now, showing a placeholder result
        result = f"Fastest path from {start} to {dest}:\n\n"
        result += f"{start} → Main Avenue → Shuttle Stop → {dest}\n"
        result += f"Estimated time: 12 minutes"
        
        self.result_text.setText(result)
        
    def go_back(self):
        from main_menu import MainPage  # Import here to avoid circular import
        self.main_menu = MainPage()
        self.main_menu.show()
        self.close()