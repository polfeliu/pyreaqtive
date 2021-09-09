import random
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton

from pyreaqtive.layouts import RQHBoxLayout
from pyreaqtive.models import RQList, RQModel, RQComputedList


class Number(RQModel):

    def __init__(self):
        super(Number, self).__init__()
        self.number = random.randint(0, 100)

    @property
    def is_odd(self):
        return self.number % 2 != 0


class ItemWidget(QWidget):

    def __init__(self, model: Number, list_model: RQList):
        super().__init__()

        self.model = model
        self.list_model = list_model

        self.main_layout = QVBoxLayout(self)
        self.resize(200, 200)

        self.number_label = QLabel(f"{model.number}")
        self.main_layout.addWidget(self.number_label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.all_numbers = RQList()
        self.odd_numbers = RQComputedList(
            lambda numbers: [number for number in numbers if number.is_odd],
            numbers=self.all_numbers
        )
        self.even_numbers = RQComputedList(
            lambda numbers: [number for number in numbers if not number.is_odd],
            numbers=self.all_numbers
        )

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        layout.addWidget(QLabel("all numbers"))
        all_numbers_display = RQHBoxLayout(
            model=self.all_numbers,
            widget=self.widget_callback
        )
        layout.addLayout(all_numbers_display)

        layout.addWidget(QLabel("odd numbers"))
        odd_numbers_display = RQHBoxLayout(
            model=self.odd_numbers,
            widget=ItemWidget
        )
        layout.addLayout(odd_numbers_display)

        layout.addWidget(QLabel("even numbers"))
        even_numbers = RQHBoxLayout(
            model=self.even_numbers,
            widget=ItemWidget
        )
        layout.addLayout(even_numbers)

    def widget_callback(self, model: RQModel, list: RQList) -> QLabel:
        if not isinstance(model, Number):
            raise TypeError

        return QLabel(f"{model.number}")

    @pyqtSlot()
    def add_item(self):
        self.all_numbers.append(
            Number()
        )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
