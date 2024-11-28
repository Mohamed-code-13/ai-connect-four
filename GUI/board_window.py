from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QStackedWidget, QGridLayout
from PyQt5.QtCore import Qt

from connect_4_solver.engine import Engine

from .cell import Cell


class BoardWindow(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.engine = Engine('0' * 42)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Connect 4 AI - Game Board")

        self.rows = 6
        self.cols = 7
        self.turn = self.settings['starting_player']
        self.human_score = 0
        self.computer_score = 0

        self.computer_label = QLabel(f"Computer: {self.computer_score}")
        self.human_label = QLabel(f"Human: {self.human_score}")
        self.turn_label = QLabel(f"Turn: {self.turn}")

        self.computer_label.setAlignment(Qt.AlignCenter)
        self.human_label.setAlignment(Qt.AlignCenter)
        self.turn_label.setAlignment(Qt.AlignCenter)

        self.grid_layout, self.cells = self.create_board()

        layout = QVBoxLayout()
        layout.addWidget(self.computer_label)
        layout.addLayout(self.grid_layout)
        layout.addWidget(self.human_label)
        layout.addWidget(self.turn_label)

        self.setLayout(layout)

    def create_board(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        cells = [[0] * self.cols for _ in range(self.rows)]

        for r in range(self.rows):
            for c in range(self.cols):
                cells[r][c] = Cell(r, c, self.on_clicked)
                grid_layout.addWidget(cells[r][c], r, c)
        return grid_layout, cells

    def on_clicked(self, c):
        # if self.turn != 'Human':
        #     return

        for r in range(self.rows - 1, -1, -1):
            if not self.cells[r][c].tile:
                self.cells[r][c].tile = 'Human'
                self.cells[r][c].setStyleSheet(
                    f'background-color: {self.settings['human_color' if self.turn == 'Human' else 'computer_color']}; border: 1px solid black;')
                self.cells[r][c].update()

                self.move(r, c)

                if self.engine.check_game_end():
                    print(self.engine.get_winner())
                    break

                self.switch_turns()
                break

    def switch_turns(self):
        self.turn = 'Computer' if self.turn == 'Human' else 'Human'
        self.turn_label.setText(f'Turn: {self.turn}')

        if self.turn == 'Computer':
            self.move_computer()

    def move(self, r, c):
        player = '1' if self.turn == self.settings['starting_player'] else '2'
        position = r * self.cols + c
        self.engine.move(position, player, self.turn)

    def move_computer(self):
        pass
