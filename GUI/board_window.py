from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QStackedWidget, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from connect_4_solver.engine import Engine

from .cell import Cell


class BoardWindow(QWidget):
    def __init__(self, settings, update_tree, board='0'*42):
        super().__init__()
        self.settings = settings
        self.update_tree = update_tree
        self.engine = Engine(
            board, int(self.settings['depth']), bool(self.settings['alpha_beta']))

        self.init_ui()
        if self.turn == 'Computer':
            self.computer_move()

    def init_ui(self):
        self.setWindowTitle("Connect 4 AI - Game Board")

        self.rows = 6
        self.cols = 7
        self.turn = self.settings['starting_player']
        self.human_score = 0
        self.computer_score = 0

        scoreboard = QHBoxLayout()
        hscore = QVBoxLayout()
        cscore = QVBoxLayout()

        clabel = QLabel("COMPUTER")
        clabel.setFont(QFont("Press Start 2P", 20))
        clabel.setStyleSheet("font-size: 20px; font-weight: bold; color: #FF5733;")
        clabel.setAlignment(Qt.AlignCenter)
        cscore.addWidget(clabel)
        self.computer_label = QLabel(f"{self.computer_score}")
        self.computer_label.setFont(QFont("Press Start 2P", 20))
        self.computer_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FF5733;")
        self.computer_label.setAlignment(Qt.AlignCenter)
        cscore.addWidget(self.computer_label)

        hlabel = QLabel("HUMAN")
        hlabel.setFont(QFont("Press Start 2P", 20))
        hlabel.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E90FF;")
        hlabel.setAlignment(Qt.AlignCenter)
        hscore.addWidget(hlabel)
        self.human_label = QLabel(f"{self.human_score}")
        self.human_label.setFont(QFont("Press Start 2P", 20))
        self.human_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E90FF;")
        self.human_label.setAlignment(Qt.AlignCenter)
        hscore.addWidget(self.human_label)

        scoreboard.addLayout(hscore)
        scoreboard.addLayout(cscore)

        self.turn_label = QLabel(f"Turn: {self.turn}")
        self.turn_label.setFont(QFont("Press Start 2P", 20))
        self.turn_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.turn_label.setAlignment(Qt.AlignCenter)
        
        self.grid_layout, self.cells = self.create_board()

        layout = QVBoxLayout()
        layout.addLayout(scoreboard)
        # layout.addWidget(self.computer_label)
        layout.addWidget(self.grid_layout)
        # layout.addWidget(self.human_label)
        layout.addWidget(self.turn_label)

        self.setLayout(layout)

    def create_board(self):
        container = QWidget()
        container.setStyleSheet("background-color: #001F54;")
        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(5)
        cells = [[0] * self.cols for _ in range(self.rows)]
        i = 0

        for r in range(self.rows):
            for c in range(self.cols):
                val = self.engine.board[i]

                cells[r][c] = Cell(r, c, self.on_clicked)

                cell_size = 75  # Adjust size as needed
                cells[r][c].setFixedSize(cell_size, cell_size)

                # Apply circular style
                border_color = '#055c9d'
                background_color = self.settings['human_color'] if val == '1' else self.settings['computer_color'] if val == '2' else '#FFFFFF'
                cells[r][c].setStyleSheet(f"""
                    background-color: {background_color};
                    border: 4px solid {border_color};
                    border-radius: {cell_size // 2}px;  /* Makes it circular */
                """)

                if val == '1' or val == '2':
                    cells[r][c].tile = 'Human' if val == '1' else 'Computer'
                    cells[r][c].setStyleSheet(
                        f'background-color: {self.settings['human_color' if val == '1' else 'computer_color']}; border: 2px solid black;')
                i += 1

                grid_layout.addWidget(cells[r][c], r, c)
        container.setLayout(grid_layout)
        return container, cells

    def on_clicked(self, c):
        if self.turn != 'Human':
            return

        self.update_move(c)

    def switch_turns(self):
        self.turn = 'Computer' if self.turn == 'Human' else 'Human'
        self.turn_label.setText(f'Turn: {self.turn}')

        if self.turn == 'Computer':
            self.computer_move()

    def update_move(self, c):
        cell_size = 75
        for r in range(self.rows - 1, -1, -1):
            if not self.cells[r][c].tile:
                self.cells[r][c].tile = self.turn
                self.cells[r][c].setStyleSheet(
                    f'background-color: {self.settings['human_color' if self.turn == 'Human' else 'computer_color']}; border: 4px solid #055c9d; border-radius: {cell_size // 2}px;')
                self.cells[r][c].update()

                if self.turn == 'Human':
                    self.move(r, c)
                # else:
                #     self.computer_move()

                self.human_label.setText(
                    f'{self.engine.score['Human']}')
                self.computer_label.setText(
                    f'{self.engine.score['Computer']}')
                if self.engine.check_game_end():
                    print(self.engine.get_winner())
                    break

                self.switch_turns()
                break

    def move(self, r, c):
        player = '1'
        position = r * self.cols + c
        self.engine.move(position, player, self.turn)

    def computer_move(self):
        board = self.engine.board
        player = '2'
        res = self.engine.computer_move(player, self.turn)
        self.update_move(res['column'])
        self.update_tree(res['tree'], board)
