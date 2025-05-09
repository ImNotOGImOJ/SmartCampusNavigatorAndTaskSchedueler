import sys
import heapq
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTextEdit, QGroupBox, QGridLayout,
    QListWidget, QListWidgetItem, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal, QModelIndex
import nodes  

class HoverComboBox(QComboBox):
    hoveredItem = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self._connected = False
    def showPopup(self):
        super().showPopup()
        if not self._connected:
            self.view().entered.connect(self.on_hover)
            self._connected = True
    def on_hover(self, index: QModelIndex):
        self.hoveredItem.emit(self.itemText(index.row()))

class CampusNavigation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campus Navigation")
        self.setGeometry(300, 100, 1100, 1200)

        # ——— Building list: "Full Name (building code)" ———
        buildings = [
            "Admissions (AD)", "Anderson Family Field (AF)", "Auxiliary Services Corporation (ASC)",
            "Bookstore/TitanShop (B)", "Children's Center (CC)", "Carl's Jr. (CJ)", "College Park (CP)",
            "Clayes Performing Arts Center (CPAC)", "Computer Science (CS)", "Corporation Yard (CY)",
            "CSUF Extension and International Program (EIP)", "Dan Black Hall (DBH)", "Engineering (E)",
            "Education Classroom Building (EC)", "Eastside Parking Structure (EPS)", "East Playfield (EP)",
            "Golleher Alumni House (GAH)", "Greenhouse Complex (GC)", "Goodwin Field (GF)", "Gordan Hall (GH)",
            "Humanities-Social Sciences (H)", "Housing & Residential Engagement (HRE)", "Intramural Fields (IF)",
            "Kinesiology & Health Science (KHS)", "Langsdorf Hall (LH)", "Modular Complex (MC)",
            "McCarthy Hall (MH)", "Military Science Leadership Excellence (MS)",
            "Nutwood Parking Structure (NPS)", "Parking & Transportation Services (P)",
            "Pollak Library (PL)", "Ruby Gerontology Center (RG)", "Resident Housing (RH)",
            "State College Parking Structure (SCPS)", "Steven G. Mihaylo Hall (SGMH)",
            "Student Health & Counseling Center (SHCC)", "Student Recreation Center (SRC)",
            "Titan House (TH)", "Titan Dining Hall (TDH)", "Titan Gymnasium (TG)", "Titan Hall (THL)",
            "Titan Stadium (TS)", "Titan Sports Complex (TSC)", "Titan Softball Field (TSF)",
            "Titan Student Union (TSU)", "Titan Tennis Courts (TTC)", "Titan Track & Field (TTF)",
            "University Police (UP)", "Visual Arts Center (VA)"
        ]

        # ——— Title ———
        title = QLabel("Campus Navigation", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:24px; font-weight:bold; margin-bottom:20px;")

        # ——— Location selectors ———
        loc_group = QGroupBox("Location")
        grid = QGridLayout()
        grid.addWidget(QLabel("Start Location:"), 0, 0)
        self.start_combo = HoverComboBox()
        self.start_combo.addItems(buildings)
        grid.addWidget(self.start_combo, 0, 1)
        grid.addWidget(QLabel("Destination:"), 1, 0)
        self.dest_combo = HoverComboBox()
        self.dest_combo.addItems(buildings)
        grid.addWidget(self.dest_combo, 1, 1)
        loc_group.setLayout(grid)

        # ——— Find Path button ———
        self.find_path_button = QPushButton("Find Path")
        self.find_path_button.clicked.connect(self.find_path)
        opt_group = QGroupBox("Navigation Options")
        vopts = QVBoxLayout()
        vopts.addWidget(self.find_path_button)
        opt_group.setLayout(vopts)

        # ——— Results text area ———
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(120)

        # ——— Map widget ———
        self.graphWidget = nodes.GraphWidget()
        self.graphWidget.setFixedSize(850, 1140)

        # ——— Building List legend ———
        legend_group = QGroupBox("Building List")
        legend_list  = QListWidget()
        legend_list.setMinimumWidth(200)
        for item in buildings:
            name, code = item.rsplit(" (", 1)
            code = code.rstrip(")")
            QListWidgetItem(f"{code}: {name}", legend_list)
        legend_layout = QVBoxLayout()
        legend_layout.addWidget(legend_list)
        legend_group.setLayout(legend_layout)

        # ——— Combine map + legend side by side ———
        map_legend_layout = QHBoxLayout()
        map_legend_layout.addWidget(self.graphWidget)
        map_legend_layout.addWidget(legend_group)

        # ——— Back button ———
        back = QPushButton("Back to Main Menu")
        back.clicked.connect(self.go_back)

        # ——— Assemble main layout ———
        main = QVBoxLayout()
        main.addWidget(title)
        main.addWidget(loc_group)
        main.addWidget(opt_group)
        main.addWidget(QLabel("Navigation Results:"))
        main.addWidget(self.result_text)
        main.addLayout(map_legend_layout)
        main.addWidget(back)
        self.setLayout(main)

    def _extract_code(self, label: str) -> str:
        return label.split("(")[1].rstrip(")")

    def find_path(self):
        start_lbl = self.start_combo.currentText()
        dest_lbl  = self.dest_combo.currentText()
        start     = self._extract_code(start_lbl)
        dest      = self._extract_code(dest_lbl)

        path, dist = self._dijkstra(start, dest)
        if not path:
            self.result_text.setText("No path found.")
            self.graphWidget.highlight_path([])
            return

        # compute time at 3.65 mph to minutes
        time_min = dist / 3.65 * 60

        code_path = " → ".join(path)
        self.result_text.setText(
            f"Path from {start_lbl} to {dest_lbl}:\n\n"
            f"{code_path}\n"
            f"Distance: {dist:.2f} mi | Time: {time_min:.0f} min"
        )
        self.graphWidget.highlight_path(path)

    def _dijkstra(self, start, dest):
        G = self.graphWidget.graph
        dist = {v: float("inf") for v in G.nodes}
        prev = {}
        dist[start] = 0
        heap = [(0, start)]
        while heap:
            d_u, u = heapq.heappop(heap)
            if u == dest:
                break
            if d_u > dist[u]:
                continue
            for v, attr in G[u].items():
                alt = d_u + attr.get("weight", 1)
                if alt < dist[v]:
                    dist[v], prev[v] = alt, u
                    heapq.heappush(heap, (alt, v))
        if dest not in prev and start != dest:
            return [], 0.0
        path = [dest]
        while path[-1] != start:
            path.append(prev[path[-1]])
        path.reverse()
        return path, dist[dest]

    def go_back(self):
        from main_menu import MainPage
        self.main_menu = MainPage()
        self.main_menu.show()
        self.close()


if __name__ == "__main__":
     app = QApplication(sys.argv)
     w = CampusNavigation()
     w.show()
     sys.exit(app.exec_())
