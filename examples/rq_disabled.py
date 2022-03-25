import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from pyreaqtive.models import RQBool
from pyreaqtive.widgets import RQPushButton, RQCheckBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        state = RQBool(True)

        checkbox = RQCheckBox(state, "disable")
        layout.addWidget(checkbox)

        button = RQPushButton("Toggle checkbox to enable/disable me", rq_disabled=state)
        layout.addWidget(button)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
