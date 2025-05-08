import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel,
                             QComboBox, QTextEdit, QGroupBox, QGridLayout)
from PyQt5.QtCore import (Qt, pyqtSignal, QModelIndex, QThread)
import nodes
import heapq


class HoverComboBox(QComboBox):
    hoveredItem = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._connected = False  # Track if signal is already connected

    def showPopup(self):
        super().showPopup()
        # Connect the signal here, only once
        if not self._connected:
            self.view().entered.connect(self.on_hover)
            self._connected = True

    def on_hover(self, index: QModelIndex):
        text = self.itemText(index.row())
        self.hoveredItem.emit(text)
        print(text)


class CampusNavigation(QWidget):
    def __init__(self):
        giantArray = [
"Admissions (AD)",
"Anderson Family Field (AF)",
"Auxiliary Services Corporation (ASC)",
"Bookstore/TitanShop (B)",
"Children's Center (CC)",
"Carl's Jr. (CJ)",
"College Park (CP)",
"Clayes Performing Arts Center (CPAC)",
"Computer Science (CS)",
"Corporation Yard (CY)",
"CSUF Extension and International Program",
"Dan Black Hall (DBH)",
"Engineering (E)",
"Education Classroom Building (EC)",
"Eastside Parking Structure (EPS)",
"East Playfield (EP)",
"Golleher Alumni House (GAH)",
"Greenhouse Complex (GC)",
"Goodwin Field (GF)",
"Gordan Hall (GH)",
"Humanities-Social Sciences (H)",
"Housing & Residential Engangement (HRE)",
"Intramural Fields (IF)",
"Kinesiology & Health Science (KHS)",
"Langsdorf Hall (LH)",
"Modular Complec (MC)",
"McCarthy Hall (MH)",
"Military Science Leadership Excellence (MS)",
"Nutwood Parking Structure (NPS)",
"Parking & Transportation Services (P)",
"Pollak Library (PL)",
"Ruby Gerontology Center (RG)",
"Resident Housing (RH)",
"State College Parking Structure (SCPS)",
"Steven G. Mihaylo Hall (SGMH)",
"Student Health & Counseling Center (SHCC)",
"Student Recreation Center (SRC)",
"Titan House (TH)",
"Titan Dining Hall (TDH)", 
"Titan Gymnasium (TG)",
"Titan Hall (TH)",
"Titan Stadium",
"Titan Sports Complex (TSC)",
"Titan Softball Field (TSF)",
"Titan Student Union (TSU)",
"Titan Tennis Courts (TTC)",
"Titan Track & Field (TTF)",
"University Police (UP)",
"Visual Arts Center (VA)"
]
        

        super().__init__()
        self.setWindowTitle("Campus Navigation")
        self.setGeometry(300, 100, 900, 1200)
        
        # Create label for the title
        self.title_label = QLabel("Campus Navigation", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 15px;")
        
        # Location selection
        self.location_group = QGroupBox("Location")
        self.location_layout = QGridLayout()
        

        # Starting point
        start_label = QLabel("Start Location:")
        self.start_combo = HoverComboBox()
        self.start_combo.addItems(giantArray)
        
        # Destination point
        dest_label = QLabel("Destination:")
        self.dest_combo = HoverComboBox()
        self.dest_combo.addItems(giantArray)

        #Graph Widget
        self.graphWidget = nodes.GraphWidget()
        #self.graphWidget.setMinimumHeight(700)
        #self.graphWidget.setMinimumWidth(400)
        self.graphWidget.setFixedSize(700, 700)
        self.start_combo.hoveredItem.connect(self.handle_hover)
        self.dest_combo.hoveredItem.connect(self.handle_hover)
        # self.nodeThread = QThread()                      #move graph widget to thread
        # self.graphWidget.moveToThread(self.nodeThread)
        # self.nodeThread.finished.connect(self.graphWidget.deleteLater)
        # self.Vi.connect("function") #


        # Add to grid layout
        self.location_layout.addWidget(start_label, 0, 0)
        self.location_layout.addWidget(self.start_combo, 0, 1)
        self.location_layout.addWidget(dest_label, 1, 0)
        self.location_layout.addWidget(self.dest_combo, 1, 1)
        self.location_group.setLayout(self.location_layout)
        
        # Navigation options
        self.options_group = QGroupBox("Navigation Options")
        self.options_layout = QVBoxLayout()
        
        self.shortest_path_button = QPushButton("Find Shortest Path")
        self.shortest_path_button.clicked.connect(self.find_shortest_path)
        
        self.fastest_path_button = QPushButton("Find Fastest Path")
        self.fastest_path_button.clicked.connect(self.find_fastest_path)
        
        self.options_layout.addWidget(self.shortest_path_button)
        self.options_layout.addWidget(self.fastest_path_button)
        self.options_group.setLayout(self.options_layout)
        
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
        layout.addWidget(self.title_label)
        layout.addWidget(self.location_group)
        layout.addWidget(self.options_group)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)
        layout.addWidget(self.graphWidget)
        layout.addWidget(back_button)
        
        self.setLayout(layout)
    

    def setUpWidgets(self):
        print("")


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



#--------------------Dijkstra on self.graphWidget.graph
    def _dijkstra(self, start, dest):
        """
        Returns (path:list, total_weight:float) from start→dest using
        a hand‑rolled Dijkstra on the weighted graph in self.graphWidget.graph.
        If no path, returns ([], inf).
        """
        G = self.graphWidget.graph            # networkx.Graph
        dist  = {v: float('inf') for v in G.nodes}
        prev  = {}
        dist[start] = 0

        heap = [(0, start)]
        while heap:
            d_u, u = heapq.heappop(heap)
            if u == dest: break
            if d_u > dist[u]: continue        # stale entry
            for v, attr in G[u].items():
                w = attr.get('weight', 1)
                alt = d_u + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (alt, v))

        # reconstruct path
        if dest not in prev and start != dest:
            return [], float('inf')
        path = [dest]
        while path[-1] != start:
            path.append(prev[path[-1]])
        path.reverse()
        return path, dist[dest]

    # inside CampusNavigation
    def handle_hover(self):
        start = self.start_combo.currentText()
        dest  = self.dest_combo.currentText()

        # skip if either node isn’t in the mini‑graph
        if start not in self.graphWidget.graph or dest not in self.graphWidget.graph:
            self.graphWidget.highlight_path([])     # clear highlight
            return

        path, _ = self._dijkstra(start, dest)
        self.graphWidget.highlight_path(path)