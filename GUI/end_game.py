from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication

class GameWindow(QMainWindow):  # Assuming your game inherits from QMainWindow
    def __init__(self):
        super().__init__()
        # Your initialization code here...

    def show_winner_popup(self, winner):
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        
        if winner == "Human":
            msg.setText("Congratulations! You Won!")
            msg.setIcon(QMessageBox.Information)
        elif winner == "Computer":
            msg.setText("Game Over! You Lost.\nBetter luck next time!")
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setText("It's a Draw!")
            msg.setIcon(QMessageBox.Information)
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(lambda: QApplication.instance().quit())
        
        msg.setStyleSheet("""
            QMessageBox {
                font-family: 'Press Start 2P';
                font-size: 14px;
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #333;
                border: 2px solid #333;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: 'Press Start 2P';
                color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        msg.exec_()

        self.close()
