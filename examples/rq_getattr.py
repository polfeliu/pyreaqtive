import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel

from pyreaqtive.widgets import RQLabel, RQSpinBox
from pyreaqtive.rq_getattr import rq_getattr


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

        self.library_instance = LibraryObject()

        change_button = QPushButton("Add One")
        change_button.clicked.connect(self.add_one)
        layout.addWidget(change_button)

        reactive_attribute = rq_getattr(self.library_instance, "counter")
        label = RQLabel(reactive_attribute)
        layout.addWidget(label)
        spinbox = RQSpinBox(reactive_attribute)
        layout.addWidget(spinbox)

    def add_one(self):
        self.library_instance.add_one()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
