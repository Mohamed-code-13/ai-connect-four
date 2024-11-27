from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QStackedWidget


class BoardWindow(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Connect 4 AI - Game Board")

        layout = QVBoxLayout()
        print(self.settings)
        layout.addWidget(QLabel(f"Starting Player: {
                         self.settings['starting_player']}"))
        layout.addWidget(
            QLabel(f"Human Color: {self.settings['human_color']}"))
        layout.addWidget(
            QLabel(f"Computer Color: {self.settings['computer_color']}"))
        layout.addWidget(QLabel(f"Depth (K): {self.settings['depth']}"))
        layout.addWidget(QLabel(
            f"Alpha-Beta Pruning: {'Enabled' if self.settings['alpha_beta'] else 'Disabled'}"))

        self.setLayout(layout)
