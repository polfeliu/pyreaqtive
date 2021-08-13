import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from pyreaqtive.models import RQFloat, RQFunction
from pyreaqtive.widgets import RQDoubleSpinBox, RQLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        layout.addWidget(QLabel("Area calculation of triangle"))

        base = RQFloat(1)
        height = RQFloat(1)

        layout.addWidget(QLabel("Base"))
        base_spinbox = RQDoubleSpinBox(base)
        layout.addWidget(base_spinbox)

        layout.addWidget(QLabel("Height"))
        height_spinbox = RQDoubleSpinBox(height)
        layout.addWidget(height_spinbox)

        # Function can also be declared inplace on the widget
        area = RQFunction(
            lambda b, h: b * h / 2,
            b=base,
            h=height
        )

        layout.addWidget(QLabel("Area"))
        area_label = RQLabel(area)
        layout.addWidget(area_label)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()