import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyreaqtive.models import RQBool
from pyreaqtive.widgets import RQCheckBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Declare a bool model
        self.state = RQBool(False)

        # Create two reactive checkboxes linked to the same model
        self.checkbox_1 = RQCheckBox(self.state, "checkbox 1")
        self.checkbox_2 = RQCheckBox(self.state, "checkbox 2")
        # They will update each other through the model that represents the state

        # Add the widgets to the layout
        layout.addWidget(self.checkbox_1)
        layout.addWidget(self.checkbox_2)


def test_basic(qtbot):
    w = MainWindow()
    w.show()
    qtbot.addWidget(w)
    assert w.state.get() == False
