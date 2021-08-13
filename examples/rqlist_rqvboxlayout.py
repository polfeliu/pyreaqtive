import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from pyreaqtive.models import RQList, RQModel
from pyreaqtive.widgets import RQLabel, RQVBoxLayout

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot


class Fruit(RQModel):

    def __init__(self, name: str):
        super(Fruit, self).__init__()
        self.name = name

    def __str__(self) -> str:
        return self.name


class FruitWidget(QWidget):

    def __init__(self, model: Fruit):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(
            QLabel(str(model))
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.fruits_list = RQList()

        fruits_display = RQVBoxLayout(
            model=self.fruits_list,
            widget=FruitWidget
        )

        layout.addLayout(fruits_display)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_fruit)
        layout.addWidget(self.add_button)

    @pyqtSlot()
    def add_fruit(self):
        self.fruits_list.append(
            Fruit("asdf")
        )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
