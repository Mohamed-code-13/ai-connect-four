from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QComboBox, QSpinBox, QCheckBox, QPushButton


class PreGameWindow(QWidget):
    def __init__(self, start_game):
        super().__init__()
        self.start_game = start_game
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Connect 4 AI - Game Settings")
        self.setGeometry(700, 300, 600, 400)
        self.setStyleSheet('background-color: #f5f5f5;')

        layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.starting_player_label = QLabel("Who starts the game?")
        self.starting_player = QComboBox()
        self.starting_player.addItems(['Human', 'Computer'])

        input_layout.addWidget(self.starting_player_label)
        input_layout.addWidget(self.starting_player)

        self.player_color_label = QLabel("Choose your color:")
        self.player_color = QComboBox()
        self.player_color.addItems(['Red', 'Yellow'])

        input_layout.addWidget(self.player_color_label)
        input_layout.addWidget(self.player_color)

        self.depth_label = QLabel('Set Depth (K) for Minimax:')
        self.depth = QSpinBox()
        self.depth.setRange(1, 20)
        self.depth.setValue(5)

        input_layout.addWidget(self.depth_label)
        input_layout.addWidget(self.depth)

        self.alpha_beta_checkbox = QCheckBox("Enable Alpha-Beta Pruning")
        self.alpha_beta_checkbox.setChecked(True)

        input_layout.addWidget(self.alpha_beta_checkbox)

        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_board)

        button_layout.addWidget(self.start_button)

        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def start_board(self):
        starting_player = self.starting_player.currentText()
        human_color = self.player_color.currentText()
        computer_color = 'Red' if human_color == 'Yellow' else 'Yellow'
        depth = self.depth.value()
        alpha_beta = self.alpha_beta_checkbox.isChecked()

        self.start_game(
            starting_player=starting_player,
            human_color=human_color,
            computer_color=computer_color,
            depth=depth,
            alpha_beta=alpha_beta
        )
