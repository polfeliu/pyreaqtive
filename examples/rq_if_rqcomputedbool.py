import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from pyreaqtive.models import RQBool, RQComputedBool
from pyreaqtive.widgets import RQLabel, RQCheckbox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        state_1 = RQBool(True)
        state_2 = RQBool(True)

        checkbox_1 = RQCheckbox(state_1, "state 1")
        layout.addWidget(checkbox_1)

        checkbox_2 = RQCheckbox(state_2, "state 2")
        layout.addWidget(checkbox_2)

        message = RQLabel("Set both checkboxes to display me", rq_if=RQComputedBool(
            lambda s1, s2: s1 and s2, s1=state_1, s2=state_2
        ))
        layout.addWidget(message)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
