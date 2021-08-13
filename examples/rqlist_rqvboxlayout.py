import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from pyreaqtive.models import RQList, RQModel
from pyreaqtive.widgets import RQLabel, RQVBoxLayout

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
import random


class Fruit(RQModel):

    def __init__(self, name: str):
        super(Fruit, self).__init__()
        self.name = name

    def __str__(self) -> str:
        return self.name


class FruitWidget(QWidget):

    def __init__(self, model: Fruit, list_model: RQList):
        super().__init__()
        self.model = model
        self.list_model = list_model
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(
            QLabel(str(model))
        )

        self.remove_button = QPushButton("remove")
        self.remove_button.clicked.connect(self.remove)
        self.main_layout.addWidget(self.remove_button)

    @pyqtSlot()
    def remove(self):
        self.list_model.remove_item(self.model)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.fruits_list = RQList()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_fruit)
        layout.addWidget(self.add_button)

        self.clear_all_button = QPushButton("Clear")
        self.clear_all_button.clicked.connect(
            lambda : self.fruits_list.clear()
        )
        layout.addWidget(self.clear_all_button)

        fruits_display = RQVBoxLayout(
            model=self.fruits_list,
            widget=FruitWidget
        )

        layout.addLayout(fruits_display)

    @pyqtSlot()
    def add_fruit(self):
        possible_fruits = [
            'apple',
            'pear',
            'apricot',
            'banana',
            'mango',
            'watermelon',
            'kumquat',
            'pineapple'
        ]
        self.fruits_list.append(
            Fruit(
                random.choice(possible_fruits)
            )
        )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
