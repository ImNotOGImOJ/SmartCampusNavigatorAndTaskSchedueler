import sys
import networkx as nx
import matplotlib.image as mpimg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent

class GraphWidget(QWidget):
    """Campus map overlay with pan/zoom and path highlighting."""

    MAP_FILE = "campusMap1.png"
    EXTENT   = [0, 900, 0, 1500]   # [x_min, x_max, y_min, y_max]

    def __init__(self, parent=None):
        super().__init__(parent)

        # — Matplotlib setup —
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax     = self.figure.add_subplot(111)
        self.ax.axis("off")

        # — Background image —
        self.img = mpimg.imread(self.MAP_FILE)
        self.ax.imshow(self.img, extent=self.EXTENT, zorder=0)

        # — Layout —
        lay = QVBoxLayout()
        lay.addWidget(self.canvas)
        self.setLayout(lay)

        # — Graph data —
        self.graph = self._create_graph()
        self.pos   = self._node_positions()

        # — Interaction state —
        self.panning   = False
        self.pan_start = None

        # — Initial draw & events —
        self.highlight_path([])
        self._connect_events()

    def _create_graph(self):
        G = nx.Graph()
        # All weights are in miles (e.g. 0.05 = 0.05 mi)
        edges = [
            ("AD","LH",0.05),("AD","SGMH",0.08),("AD","GH",0.10),("AD","CJ",0.09),
            ("MH","LH",0.15),("MH","GH",0.15),("DBH","LH",0.16),("DBH","MH",0.06),
            ("MH","H",0.16),("H","EPS",0.16),("GH","EPS",0.17),("H","PL",0.12),
            ("H","EC",0.10),("EPS","EC",0.21),("PL","EC",0.10),("E","EC",0.10),
            ("CS","E",0.50),("CS","TDH",0.10),("E","TDH",0.11),("EPS","CS",0.25),
            ("TDH","RG",0.12),("RH","TDH",0.09),("SHCC","RH",0.25),("SHCC","E",0.19),
            ("SHCC","PL",0.24),("SHCC","EC",0.22),("EP","RG",0.20),("EP","SHCC",0.19),
            ("TG","EP",0.16),("KHS","TG",0.04),("IF","TG",0.13),("IF","EP",0.15),
            ("TTC","TTF",0.14),("TTF","IF",0.13),("TTC","IF",0.11),("TTC","TG",0.16),
            ("EP","TSF",0.14),("TTF","TSF",0.14),("TSC","TTF",0.09),("TSF","TSC",0.09),
            ("TSC","AF",0.09),("GF","TSC",0.11),("GF","AF",0.10),("TS","GF",0.13),
            ("TS","TSC",0.13),("CC","TS",0.15),("TTC","CC",0.17),("TTC","CY",0.15),
            ("TTC","SRC",0.12),("SCPS","SRC",0.06),("CY","SCPS",0.10),("TSU","SCPS",0.11),
            ("TSU","B",0.12),("VA","TSU",0.08),("CY","UP",0.10),("GAH","UP",0.06),
            ("UP","SCPS",0.04),("SCPS","GAH",0.05),("TH","TSU",0.10),("TH","VA",0.07),
            ("ASC","TH",0.05),("VA","NPS",0.14),("TH","VA",0.08),("GC","NPS",0.12),
            ("GC","CPAC",0.07),("CPAC","B",0.09),("CPAC","PL",0.11),("B","PL",0.08),
            ("KHS","B",0.07),("KHS","PL",0.09),("CPAC","MH",0.09),
        ]
        G.add_weighted_edges_from(edges)
        return G

    def _node_positions(self):
        # Pixel coords on campusMap1.png
        return {
            'AD': (575,390), 'AF': (520,1140), 'ASC':(45,634),  'B':  (347,689),
            'CC': (215,1110),'CJ': (604,429),  'CP': (630,200),  'CPAC':(360,544),
            'CS': (700,735), 'CY': (154,959),  'DBH':(410,405), 'E':   (655,735),
            'EC': (570,630), 'EPS':(760,520),  'EP': (490,930),  'GAH': (150,740),
            'GC': (335,453), 'GH': (573,458),  'GF': (485,1250), 'H':   (584,545),
            'HRE':(787,880),'IF': (430,930),  'KHS':(410,780),  'LH':  (533,391),
            'MC': (440,352), 'MH': (461,457),  'MS': (580,940),  'NPS': (212,405),
            'P':   (65,634), 'PL': (477,648),  'RG': (655,870),  'RH':  (750,889),
            'SCPS':(200,830),'SGMH':(608,352), 'SHCC':(578,800),'SRC': (280,830),
            'TH':  (91,596), 'TDH':(750,828),  'TG': (430,820),  'TS':  (360,1200),
            'TSC': (452,1108),'TSF':(547,1055),'TSU':(200,680), 'TTC': (343,936),
            'TTF': (415,1042),'UP': (150,820),  'VA': (175,580),
        }

    def _connect_events(self):
        c = self.canvas.mpl_connect
        c("scroll_event",        self._on_scroll)
        c("button_press_event",  self._on_press)
        c("motion_notify_event", self._on_motion)
        c("button_release_event",self._on_release)

    def _on_scroll(self, ev):
        sf  = 1.2 if ev.button=='up' else 1/1.2
        if ev.xdata is None or ev.ydata is None: return
        x,y = ev.xdata, ev.ydata
        xl,xr = self.ax.get_xlim(); yl,yr = self.ax.get_ylim()
        self.ax.set_xlim(x-(x-xl)*sf, x+(xr-x)*sf)
        self.ax.set_ylim(y-(y-yl)*sf, y+(yr-y)*sf)
        self.canvas.draw()

    def _on_press(self, ev: MouseEvent):
        if ev.button!=1 or ev.inaxes!=self.ax: return
        self.panning, self.pan_start = True, (ev.x, ev.y)
        self.orig_xlim, self.orig_ylim = self.ax.get_xlim(), self.ax.get_ylim()

    def _on_motion(self, ev: MouseEvent):
        if not self.panning or ev.x is None: return
        dx,dy = ev.x-self.pan_start[0], ev.y-self.pan_start[1]
        xl,xr = self.orig_xlim; yl,yr = self.orig_ylim
        dx_d = dx*(xr-xl)/self.canvas.width()
        dy_d = dy*(yr-yl)/self.canvas.height()
        self.ax.set_xlim(xl-dx_d, xr-dx_d)
        self.ax.set_ylim(yl+dy_d, yr+dy_d)
        self.canvas.draw()

    def _on_release(self, ev):
        self.panning = False

    def highlight_path(self, path):
        """Draw map+graph, highlight nodes in `path` in green."""
        self.ax.clear()
        self.ax.imshow(self.img, extent=self.EXTENT, zorder=0)

        # draw all edges & nodes
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax,
                               edge_color="#aaa", width=2)
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax,
                               node_color="#f39c12", node_size=300)
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax,
                               font_size=8, font_color="white")

        if path:
            # highlight edges
            ed = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax,
                                   edgelist=ed, edge_color="#27ae60", width=6)
            # highlight nodes
            nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax,
                                   nodelist=[path[0]], node_color="#2ecc71", node_size=450)
            nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax,
                                   nodelist=[path[-1]], node_color="#e74c3c", node_size=450)

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gw = GraphWidget()
    gw.resize(800,600)
    gw.show()
    sys.exit(app.exec_())
