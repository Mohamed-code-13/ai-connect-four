from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class Displayer(QWidget):
    def __init__(self):
        super().__init__()
        self.expanded_nodes = 0
        self.time_taken = 0.0

        self.nodes_label = QLabel(f"Nodes Expanded: {self.expanded_nodes}")
        self.time_label = QLabel(f"Time Taken: {self.time_taken:.2f} seconds")

        self.nodes_label.setAlignment(Qt.AlignLeft)
        self.time_label.setAlignment(Qt.AlignLeft)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.nodes_label)
        self.layout.addWidget(self.time_label)

        self.setLayout(self.layout)

    def update_stats(self, expanded_nodes, time_taken):
        self.expanded_nodes = expanded_nodes
        self.time_taken = time_taken

        self.nodes_label.setText(f"Nodes Expanded: {self.expanded_nodes}")
        self.time_label.setText(f"Time Taken: {self.time_taken:.2f} seconds")