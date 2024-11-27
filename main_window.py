from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QStackedWidget

from board_window import BoardWindow
from pre_game_window import PreGameWindow


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
        self.board_window = BoardWindow(settings)
        self.stack.addWidget(self.board_window)
        self.stack.setCurrentWidget(self.board_window)
