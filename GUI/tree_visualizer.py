from PyQt5.QtWidgets import QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout,  QWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from GUI.cell import Cell


class ClickableWidget(QWidget):
    clicked = pyqtSignal()  # Define a custom signal

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        print("CLICKED")
        super().mousePressEvent(event)
        self.clicked.emit()


class TreeVisualizer(QWidget):
    def __init__(self, settings, board, tree={}):
        super().__init__()
        self.settings = settings
        self.board = board
        self.tree = tree
        self.rows = 6
        self.cols = 7
        self.arr = []
        self.prev = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.init_ui()

    def init_ui(self):

        for w in self.arr:
            self.layout.removeWidget(w)
            w.deleteLater()
        self.arr = []

        if not self.tree or self.board not in self.tree:
            return

        # for w in self.arr:
        #     self.layout.removeWidget(w)
        # self.arr = []
        grid_layout, _ = self.create_board(self.board)
        # widget = QWidget()
        # widget.setLayout(grid_layout)
        grid_layout.setFixedSize(20 * self.cols, 20 * self.rows)

        curr_label = QLabel(f"Eval: {self.tree[self.board]['score']}\nAlpha: {self.tree[self.board]['alpha']}\nBeta: {self.tree[self.board]['beta']}")
        curr_label.setAlignment(Qt.AlignCenter)
        
        v = QVBoxLayout()
        v.addWidget(grid_layout, alignment=Qt.AlignCenter)
        v.addWidget(curr_label)

        self.arr.append(grid_layout)
        self.arr.append(curr_label)
        self.layout.addLayout(v)
        # self.layout.addWidget(grid_layout, alignment=Qt.AlignCenter)

        if 'children' not in self.tree[self.board]:
            return
        
        # data_label = QLabel(f"Eval: {self.board['eval']}\nAlpha: {self.board['alpha']}\nBeta: {self.board['beta']}")
        # data_label.setAlignment(Qt.AlignCenter)

        h = QHBoxLayout()
        for nei, eval in self.tree[self.board]['children']:
            grid_layout1, self.cells = self.create_board(nei)
            widget1 = self.make_clickable(grid_layout1)
            # widget1.setLayout(grid_layout1)
            widget1.setFixedSize(20 * self.cols, 20 * self.rows)
            widget1.clicked.connect(
                lambda nei_val=nei: (self.prev.append(self.board), self.expand_node(nei_val)))
            # widget1.clicked.connect(
            #     lambda nei_val=nei: self.expand_node(nei_val))

            data_label = QLabel(f"Eval: {eval}\nAlpha: {self.tree[self.board]['alpha']}\nBeta: {self.tree[self.board]['beta']}")
            data_label.setAlignment(Qt.AlignCenter)

            vbox = QVBoxLayout()
            vbox.addWidget(widget1, alignment=Qt.AlignCenter)
            vbox.addWidget(data_label, alignment=Qt.AlignCenter)

            container_widget = QWidget()
            container_widget.setLayout(vbox)
            h.addWidget(container_widget, alignment=Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(h)

        self.arr.append(widget)
        self.layout.addWidget(widget)

        go_back_button = QPushButton("Go Back")
        go_back_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                border: 2px solid #333;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: 'Press Start 2P';
                color: #f0f0f0;
            }
        """)
        go_back_button.clicked.connect(self.go_back)

        stats_label = QLabel(f"Expanded Nodes: {self.expanded_nodes}\n\nTime: {self.time:.3f} seconds")
        stats_label.setAlignment(Qt.AlignLeft)
        stats_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                font-size: 14px;
                font-family: 'Press Start 2P';
                color: #333;
            }
        """)

        self.arr.append(go_back_button)
        self.arr.append(stats_label)
        self.layout.addWidget(go_back_button, alignment=Qt.AlignCenter)
        self.layout.addWidget(stats_label)
    
    def make_clickable(self, widget):
        clickable = ClickableWidget()
        
        clickable.setGeometry(widget.geometry())
        if widget.parent():
            widget.setParent(clickable)

        layout = QVBoxLayout(clickable)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)

        return clickable
    
    def create_board(self, state):
        container = QWidget()
        container.setStyleSheet("background-color: #001F54;")
        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(0)
        cells = [[0] * self.cols for _ in range(self.rows)]
        i = 0

        for r in range(self.rows):
            for c in range(self.cols):
                val = state[i]

                cells[r][c] = Cell(r, c, self.on_clicked, 20, 20)

                cell_size = 15  # Adjust size as needed
                cells[r][c].setFixedSize(cell_size, cell_size)

                # Apply circular style
                border_color = '#001F54'  # Oxford Blue
                background_color = self.settings['human_color'] if val == '1' else self.settings['computer_color'] if val == '2' else '#FFFFFF'
                cells[r][c].setStyleSheet(f"""
                    background-color: {background_color};
                    border: 2px solid {border_color};
                    border-radius: {cell_size // 2}px;  /* Makes it circular */
                """)

                if val == '1' or val == '2':
                    cells[r][c].tile = 'Human' if val == '1' else 'Computer'
                    cells[r][c].setStyleSheet(
                        f'background-color: {self.settings['human_color' if val == '1' else 'computer_color']}; border: 2px solid black; border-radius: {cell_size // 2}px;')
                i += 1

                grid_layout.addWidget(cells[r][c], r, c)
        container.setLayout(grid_layout)
        return container, cells

    def on_clicked(self, c):
        pass

    def update_tree(self, tree, board, expanded_nodes, time):
        self.tree = tree
        self.board = board
        self.expanded_nodes = expanded_nodes
        self.time = time
        self.init_ui()
        self.update()

    def expand_node(self, state):
        self.board = state
        self.init_ui()
        self.update()

    def go_back(self):
        if self.prev:
            self.board = self.prev.pop()
            self.init_ui()
            self.update()