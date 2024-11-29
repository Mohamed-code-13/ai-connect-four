from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout,  QWidget, QLabel
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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.init_ui()

    def init_ui(self):

        if not self.tree or self.board not in self.tree:
            return

        for w in self.arr:
            self.layout.removeWidget(w)
        self.arr = []

        grid_layout, _ = self.create_board(self.board)
        widget = QWidget()
        widget.setLayout(grid_layout)
        widget.setFixedSize(20 * self.cols, 20 * self.rows)

        self.arr.append(widget)
        self.layout.addWidget(widget, alignment=Qt.AlignCenter)

        h = QHBoxLayout()
        for nei, eval in self.tree[self.board]['children']:
            grid_layout1, self.cells = self.create_board(nei)
            widget1 = ClickableWidget()
            widget1.setLayout(grid_layout1)
            widget1.setFixedSize(20 * self.cols, 20 * self.rows)
            widget1.clicked.connect(
                lambda nei_val=nei: self.expand_node(nei_val))

            eval_label = QLabel(f"Eval: {eval}")
            eval_label.setAlignment(Qt.AlignCenter)

            vbox = QVBoxLayout()
            vbox.addWidget(widget1, alignment=Qt.AlignCenter)
            vbox.addWidget(eval_label, alignment=Qt.AlignCenter)

            container_widget = QWidget()
            container_widget.setLayout(vbox)
            h.addWidget(container_widget, alignment=Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(h)

        self.arr.append(widget)
        self.layout.addWidget(widget)

    def create_board(self, state):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        cells = [[0] * self.cols for _ in range(self.rows)]
        i = 0

        for r in range(self.rows):
            for c in range(self.cols):
                val = state[i]

                cells[r][c] = Cell(r, c, self.on_clicked, 20, 20)
                if val == '1' or val == '2':
                    cells[r][c].tile = 'Human' if val == '1' else 'Computer'
                    cells[r][c].setStyleSheet(
                        f'background-color: {self.settings['human_color' if val == '1' else 'computer_color']}; border: 1px solid black;')
                i += 1

                grid_layout.addWidget(cells[r][c], r, c)
        return grid_layout, cells

    def on_clicked(self, c):
        pass

    def update_tree(self, tree, board):
        self.tree = tree
        self.board = board
        self.init_ui()
        self.update()

    def expand_node(self, state):
        self.board = state
        self.init_ui()
        self.update()
