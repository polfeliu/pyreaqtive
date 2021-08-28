import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from pyreaqtive.models import RQInt, RQBool
from pyreaqtive.widgets import RQSpinBox, RQLabel, RQCheckbox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        state = RQBool(True)

        checkbox = RQCheckbox(state, "show message")
        layout.addWidget(checkbox)

        message = RQLabel("Toggle checkbox to hide/show me", rq_if=state)
        layout.addWidget(message)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
