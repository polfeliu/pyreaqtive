import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

from pyreaqtive.models import RQFloat
from pyreaqtive.rq_connect import RQConnect, LinearConversion
from pyreaqtive.widgets import RQDoubleSpinBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        celsius = RQFloat(1)
        fahrenheit = RQFloat(1)

        layout.addWidget(QLabel("Celsius"))
        celsius_spinbox = RQDoubleSpinBox(celsius)
        celsius_spinbox.setMinimum(-10000)
        celsius_spinbox.setMaximum(10000)
        layout.addWidget(celsius_spinbox)

        layout.addWidget(QLabel("Fahrenheit"))
        fahrenheit_spinbox = RQDoubleSpinBox(fahrenheit)
        fahrenheit_spinbox.setMinimum(-10000)
        fahrenheit_spinbox.setMaximum(10000)
        layout.addWidget(fahrenheit_spinbox)

        self.connect = RQConnect(
            model_a=celsius,
            model_b=fahrenheit,
            conversion=LinearConversion(
                scale_a_to_b=9 / 5,
                offset_a_to_b=32
            )
        )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
