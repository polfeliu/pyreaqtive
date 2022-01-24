import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from pyreaqtive.models import RQFloat
from pyreaqtive.widgets import RQDoubleSpinBox, RQLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        number = RQFloat(1)

        number_spinbox1 = RQDoubleSpinBox(number)
        layout.addWidget(number_spinbox1)

        # Second Double Spinbox wait for user to press enter or lose focus
        number_spinbox2 = RQDoubleSpinBox(number, wait_for_finish=True)
        layout.addWidget(number_spinbox2)

        number_label = RQLabel(number)
        layout.addWidget(number_label)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
