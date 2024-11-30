from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QComboBox, QSpinBox, QCheckBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

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

        self.title = QLabel("GAME SETTINGS")
        self.title.setFont(QFont("Press Start 2P", 16))
        input_layout.addWidget(self.title)

        self.starting_player_label = QLabel("STARTING PLAYER")
        self.starting_player_label.setFont(QFont("Press Start 2P", 12))
        self.starting_player = QComboBox()
        self.starting_player.addItems(['Human', 'Computer'])
        self.starting_player.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0;
                border: 2px solid #333;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: 'Press Start 2P';
                color: #333;
            }
        """)

        starter = QVBoxLayout()
        starter.addWidget(self.starting_player_label)
        starter.addWidget(self.starting_player)
        starter.setSpacing(0)
        input_layout.addLayout(starter)

        self.player_color_label = QLabel("CHOOSE YOUR COLOUR")
        self.player_color_label.setFont(QFont("Press Start 2P", 12))
        self.player_color = QComboBox()
        self.player_color.addItems(['Red', 'Yellow'])
        self.player_color.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0;
                border: 2px solid #333;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: 'Press Start 2P';
                color: #333;
            }
        """)

        your_colour = QVBoxLayout()
        your_colour.addWidget(self.player_color_label)
        your_colour.addWidget(self.player_color)
        your_colour.setSpacing(0)
        input_layout.addLayout(your_colour)

        self.depth_label = QLabel('DEPTH (K) OF MINIMAX')
        self.depth_label.setFont(QFont("Press Start 2P", 12))
        self.depth = QSpinBox()
        self.depth.setStyleSheet("""
            QSpinBox {
                background-color: #f0f0f0;
                border: 2px solid #333;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: 'Press Start 2P';
                color: #333;
            }
        """)
        self.depth.setRange(1, 20)
        self.depth.setValue(5)

        minimax_depth = QVBoxLayout()
        minimax_depth.addWidget(self.depth_label)
        minimax_depth.addWidget(self.depth)
        minimax_depth.setSpacing(0)
        input_layout.addLayout(minimax_depth)

        self.alpha_beta_checkbox = QCheckBox("Enable Alpha-Beta Pruning")
        self.alpha_beta_checkbox.setStyleSheet("""
            QCheckBox {
                background-color: #f0f0f0;
                padding-top: 10px;
                padding-bottom: 10px;
                font-size: 10px;
                font-family: 'Press Start 2P';
                color: #333;
            }
        """)
        self.alpha_beta_checkbox.setChecked(True)

        input_layout.addWidget(self.alpha_beta_checkbox)

        self.start_button = QPushButton("Start Game")
        self.start_button.setStyleSheet("""
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
        self.start_button.clicked.connect(self.start_board)

        button_layout.addWidget(self.start_button)

        # layout.addWidget(self.title)
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
