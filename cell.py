from PyQt5.QtWidgets import QFrame


class Cell(QFrame):
    def __init__(self, row, col, on_clicked):
        super().__init__()

        self.row = row
        self.col = col
        self.on_clicked = on_clicked

        self.setFixedSize(80, 80)
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.tile = None

    def mousePressEvent(self, event):
        self.on_clicked(self.col)
        self.update()
