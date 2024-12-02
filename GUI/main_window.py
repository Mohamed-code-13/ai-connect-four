from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout,  QWidget, QApplication, QStackedWidget, QPushButton

from GUI.tree_visualizer import TreeVisualizer

from .board_window import BoardWindow
from .pre_game_window import PreGameWindow
from .display_data import Displayer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Connect 4 AI")
        self.setGeometry(700, 300, 600, 400)
        self.setStyleSheet('background-color: #f5f5f5;')

        self.stack = QStackedWidget()
        self.pre_game_window = PreGameWindow(self.start_game)
        self.stack.addWidget(self.pre_game_window)
        self.stack.setCurrentWidget(self.pre_game_window)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        # self.setLayout(main_layout)
        l = QWidget()
        l.setLayout(main_layout)
        self.setCentralWidget(l)

    def start_game(self, **settings):
        # self.board_window = BoardWindow(settings)
        # self.stack.addWidget(self.board_window)
        # self.stack.setCurrentWidget(self.board_window)
        tree_visualizer = TreeVisualizer(settings,
                                         '000000000000000012000002100000122000211201')
        board = BoardWindow(settings, tree_visualizer.update_tree)
        board.setFixedSize(600, 600)

        side_panel = QVBoxLayout()
        side_panel.addWidget(tree_visualizer)

        row = QHBoxLayout()
        row.addWidget(board)
        row.addLayout(side_panel)

        w = QWidget()
        w.setLayout(row)
        self.stack.addWidget(w)
        self.stack.setCurrentWidget(w)
