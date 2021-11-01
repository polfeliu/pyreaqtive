import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton

from pyreaqtive.rq_getattr import rq_getattr
from pyreaqtive.widgets import RQLabel, RQSpinBox


# Example class that is on a library that doesn't use pyreaqtive models
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

        # Create a instance of the library object, as usual
        self.library_instance = LibraryObject()

        # Some Internal functionality of the library, connected to a button to demostrate
        change_button = QPushButton("Add One")
        change_button.clicked.connect(self.add_one)
        layout.addWidget(change_button)

        # Get a reactive attribute, an RQObject that will be updated everytime the library attribute is updated
        reactive_attribute = rq_getattr(self.library_instance, "counter")

        # link to a label to display
        label = RQLabel(reactive_attribute)
        layout.addWidget(label)

        # Or link to a Spinbox that displays it and also allows to modify the RQObject and the attribute of the instance
        spinbox = RQSpinBox(reactive_attribute)
        layout.addWidget(spinbox)

    def add_one(self):
        self.library_instance.add_one()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
