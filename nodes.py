import sys
import networkx as nx
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent
import matplotlib.image as mpimg

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.img = mpimg.imread('campusMap1.png')
        x_min, x_max, y_min, y_max = 0, 900, 0, 1500
        self.extent=[x_min, x_max, y_min, y_max]

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.graph = self.create_graph()
        self.pos = self.custom_node_positions()

        self.panning = False
        self.pan_start = None

        # self.backgroundLabel = QLabel(self)
        #self.layout.setStyleSheet("background-image : url(campusMap1.png); border : 2px solid blue") 


        #self._draw_graph()
        self.highlight_path([])
        self._connect_events()

    def create_graph(self):
        # Create a weighted graph
        G = nx.Graph()

        #   G.add_edge('', '', weight=)

        #AD
        G.add_edge('AD', 'LH', weight=0)
        G.add_edge('AD', 'SGMH', weight=1)
        G.add_edge('AD', 'GH', weight=1)
        G.add_edge('AD', 'CJ', weight=1)
        G.add_edge('MH', 'LH', weight=3)
        G.add_edge('MH', 'GH', weight=4)
        G.add_edge('DBH', 'LH', weight=3)
        G.add_edge('DBH', 'MH', weight=2)
        G.add_edge('MH', 'H', weight=4)
        G.add_edge('MH', 'H', weight=3)
        G.add_edge('H', 'EPS', weight=20)
        G.add_edge('GH', 'EPS', weight=20)
        G.add_edge('H', 'PL', weight=8)
        G.add_edge('H', 'EC', weight=6)
        G.add_edge('EPS', 'EC', weight=21)
        G.add_edge('PL', 'EC', weight=4)
        G.add_edge('E', 'EC', weight=10)
        G.add_edge('CS', 'E', weight=1)
        G.add_edge('CS', 'TDH', weight=6)
        G.add_edge('E', 'TDH', weight=6)
        G.add_edge('EPS', 'CS', weight=26)
        G.add_edge('TDH', 'RG', weight=6)
        G.add_edge('RH', 'TDH', weight=3)
        G.add_edge('SHCC', 'RH', weight=4)
        G.add_edge('SHCC', 'E', weight=4)
        G.add_edge('SHCC', 'PL', weight=6)
        G.add_edge('SHCC', 'EC', weight=6)
        G.add_edge('EP', 'RG', weight=12)
        G.add_edge('EP', 'SHCC', weight=9)
        G.add_edge('TG', 'EP', weight=3)
        G.add_edge('KHS', 'TG', weight=0)
        G.add_edge('IF', 'TG', weight=3)
        G.add_edge('IF', 'EP', weight=3)
        G.add_edge('TTC', 'TTF', weight=2)
        G.add_edge('TTF', 'IF', weight=2)
        G.add_edge('TTC', 'IF', weight=3)
        G.add_edge('TTC', 'TG', weight=3)
        G.add_edge('EP', 'TSF', weight=4)
        G.add_edge('TTF', 'TSF', weight=3)
        G.add_edge('TSC', 'TTF', weight=2)
        G.add_edge('TSF', 'TSC', weight=3)
        G.add_edge('TSC', 'AF', weight=2)
        G.add_edge('GF', 'TSC', weight=4)
        G.add_edge('GF', 'AF', weight=2)
        G.add_edge('TS', 'GF', weight=5)
        G.add_edge('TS', 'TSC', weight=4)
        G.add_edge('CC', 'TS', weight=10)
        G.add_edge('TTC', 'CC', weight=13)
        G.add_edge('TTC', 'CY', weight=12)
        G.add_edge('TTC', 'SRC', weight=6)
        G.add_edge('SCPS', 'SRC', weight=1)
        G.add_edge('CY', 'SCPS', weight=4)
        G.add_edge('TSU', 'SCPS', weight=4)
        G.add_edge('TSU', 'B', weight=8)
        G.add_edge('VA', 'TSU', weight=5)
        G.add_edge('CY', 'UP', weight=5)
        G.add_edge('GAH', 'UP', weight=3)
        G.add_edge('UP', 'SCPS', weight=3)
        G.add_edge('SCPS', 'GAH', weight=3)
        G.add_edge('TH', 'TSU', weight=6)
        G.add_edge('TH', 'VA', weight=3)
        G.add_edge('ASC', 'TH', weight=2)
        G.add_edge('VA', 'NPS', weight=5)
        G.add_edge('TH', 'VA', weight=5)
        G.add_edge('GC', 'NPS', weight=3)
        G.add_edge('GC', 'CPAC', weight=3)
        G.add_edge('CPAC', 'B', weight=6)
        G.add_edge('CPAC', 'PL', weight=5)
        G.add_edge('B', 'PL', weight=4)
        G.add_edge('KHS', 'B', weight=3)
        G.add_edge('KHS', 'PL', weight=4)
        G.add_edge('CPAC', 'MH', weight=3)


        #G.add_edge('', '', weight=)
        return G

    def custom_node_positions(self):
        # Define exact node positions here
        return {
                #   x,  Y
            'AD': (575, 390),    # Admissions
            'AF': (520, 1140),            # Anderson Family Field
            'ASC': (45, 634),           # Auxiliary Services Corporation
            'B': (347, 689),             # Bookstore/TitanShop
            'CC': (215, 1110),            # Children's Center
            'CJ': (604, 429),    # Carl's Jr.
            'CP': (630, 200),            # College Park
            'CPAC': (360, 544),          # Clayes Performing Arts Center
            'CS': (700, 735),            # Computer Science
            'CY': (154, 959),            # Corporation Yard
            'DBH': (410, 405),           # Dan Black Hall
            'E': (655, 735),             # Engineering
            'EC': (570, 630),            # Education Classroom Building
            'EPS': (760, 520),           # Eastside Parking Structure
            'EP': (490, 930),            # East Playfield
            'GAH': (150, 740),           # Golleher Alumni House
            'GC': (335, 453),                      #Greenhouse Complex
            'GH': (573, 458),    # Gordan Hall
            'GF': (485, 1250),            # Goodwin Field
            'H': (584, 545),             # Humanities-Social Sciences
            'HRE': (787, 880),           # Housing & Residential Engagement
            'IF': (430, 930),            # Intramural Fields
            'KHS': (410, 780),           # Kinesiology & Health Science
            'LH': (533, 391),    # Langsdorf Hall
            'MC': (440, 352),            # Modular Complex
            'MH': (461, 457),            # McCarthy Hall
            'MS': (580, 940),            # Military Science Leadership Excellence
            'NPS': (212, 405),           # Nutwood Parking Structure
            'P': (65, 634),          # Parking & Transportation Services
            'PL': (477, 648),            # Pollak Library
            'RG': (655, 870),            # Ruby Gerontology Center
            'RH': (750, 889),            # Resident Housing
            'SCPS': (200, 830),          # State College Parking Structure
            'SGMH': (608, 352),  # Steven G. Mihaylo Hall
            'SHCC': (578, 800),          # Student Health & Counseling Center
            'SRC': (280, 830),           # Student Recreation Center
            'TH': (91, 596),            # Titan House
            'TDH': (750, 828),           # Titan Dining Hall
            'TG': (430, 820),            # Titan Gymnasium
            'TS': (360, 1200),            # Titan Stadium
            'TSC': (452, 1108),           # Titan Sports Complex
            'TSF': (547, 1055),           # Titan Softball Field
            'TSU': (200, 680),           # Titan Student Union
            'TTC': (343, 936),           # Titan Tennis Courts
            'TTF': (415, 1042),           # Titan Track & Field
            'UP': (150, 820),            # University Police
            'VA': (175, 580)            # Visual Arts Center

        }

    # replaced by highlight draw
    # can be removed
    # def _draw_graph(self):
    #     self.ax.clear()

    #     nx.draw(
    #         self.graph,
    #         pos=self.pos,
    #         ax=self.ax,
    #         with_labels=True,
    #         node_color='lightgreen',
    #         edge_color='gray',
    #         node_size=600,
    #         font_size=10
    #     )
    #     self.canvas.draw()

    def _connect_events(self):
        self.canvas.mpl_connect("scroll_event", self._on_scroll)
        self.canvas.mpl_connect("button_press_event", self._on_press)
        self.canvas.mpl_connect("motion_notify_event", self._on_motion)
        self.canvas.mpl_connect("button_release_event", self._on_release)

    def _on_scroll(self, event):
        base_scale = 1.2
        scale_factor = base_scale if event.button == 'up' else 1 / base_scale

        xdata = event.xdata
        ydata = event.ydata

        if xdata is None or ydata is None:
            return

        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()

        new_xlim = [xdata - (xdata - cur_xlim[0]) * scale_factor,
                    xdata + (cur_xlim[1] - xdata) * scale_factor]
        new_ylim = [ydata - (ydata - cur_ylim[0]) * scale_factor,
                    ydata + (cur_ylim[1] - ydata) * scale_factor]

        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()

    def _on_press(self, event: MouseEvent):
        if event.button != 1 or event.inaxes != self.ax:
            return
        self.panning = True
        self.pan_start = (event.x, event.y)  # Use pixel positions
        self.orig_xlim = self.ax.get_xlim()
        self.orig_ylim = self.ax.get_ylim()

    def _on_motion(self, event: MouseEvent):
        if self.panning and event.x is not None and event.y is not None:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]

            dx_data = dx * (self.orig_xlim[1] - self.orig_xlim[0]) / self.canvas.width()
            dy_data = dy * (self.orig_ylim[1] - self.orig_ylim[0]) / self.canvas.height()

            new_xlim = (self.orig_xlim[0] - dx_data, self.orig_xlim[1] - dx_data)
            new_ylim = (self.orig_ylim[0] + dy_data, self.orig_ylim[1] + dy_data)  # Y is inverted

            self.ax.set_xlim(new_xlim)
            self.ax.set_ylim(new_ylim)
            self.canvas.draw()

    def _on_release(self, event: MouseEvent):
        self.panning = False

    def highlight_path(self, path_nodes):
        edge_path = list(zip(path_nodes[:-1], path_nodes[1:]))

        # Draw the graph with custom highlighting
        self.ax.clear()

        #draw background
        self.ax.imshow(self.img, extent=self.extent, zorder=0)  # <-- BACKGROUND

        # Default nodes and edges
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_color='orange', node_size=300)
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, edge_color='orange', width=4)
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax, font_size=10)

        # Draw labels
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax, font_size=10)

        # Draw edge weights
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, ax=self.ax, font_size=9)

        # Highlight nodes in the path
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=path_nodes, ax=self.ax,
                            node_color='green', node_size=700)

        # Highlight edges in the path
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=edge_path, ax=self.ax,
                            edge_color='green', width=6)

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GraphWidget()
    window.setWindowTitle("Smooth Pannable NetworkX Graph in PyQt")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())