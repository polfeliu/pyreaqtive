import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel

from pyreaqtive.widgets import RQLabel
from pyreaqtive.rq_getattr import rq_getattr, reactivize


class LibraryObject:

    def __init__(self):
        self.counter = 1

    def add_one(self):
        self.counter += 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        reactivize(LibraryObject)
        self.non_reactive_object = LibraryObject()

        change_button = QPushButton("Add One")
        change_button.clicked.connect(self.add_one)
        layout.addWidget(change_button)

        reactive_attribute = rq_getattr(self.non_reactive_object, "counter")
        label = RQLabel(reactive_attribute)
        layout.addWidget(label)

    def add_one(self):
        self.non_reactive_object.add_one()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
