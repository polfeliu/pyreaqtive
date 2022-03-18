import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from pyreaqtive.models import RQBool
from pyreaqtive.widgets import RQLabel, RQCheckBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        state = RQBool(True)

        checkbox = RQCheckBox(state, "show message")
        layout.addWidget(checkbox)

        message = RQLabel("Toggle checkbox to hide/show me", rq_if=state)
        layout.addWidget(message)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
