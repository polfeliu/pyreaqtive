import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

from pyreaqtive.models import RQFloat
from pyreaqtive.rq_connect import RQConnect, Conversion
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

        # It's important to reference the connect object so it's not garbage collected
        self.connect = RQConnect(
            model_a=celsius,  # Connect to model A
            model_b=fahrenheit,  # Connect to Model B
            conversion=Conversion(  # Declare conversion formulas to convert reciprocally
                a_to_b=lambda c: c * (9 / 5) + 32,
                b_to_a=lambda f: (f - 32) / (9 / 5)
            )
        )
        # Note RQConnect only makes sense for functions that are reversible.

        # In this case we could also use LinearConversion
        # self.connect = RQConnect(
        #    model_a=celsius,
        #    model_b=fahrenheit,
        #    conversion=LinearConversion(
        #        scale_a_to_b=9 / 5,
        #        offset_a_to_b=32
        #    )
        # )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
