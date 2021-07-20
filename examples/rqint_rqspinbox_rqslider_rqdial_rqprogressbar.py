import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyreaqtive.models import RQInt
from pyreaqtive.widgets import RQSpinBox, RQSlider, RQDial, RQProgressBar
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        my_integer = RQInt(50)

        spinbox = RQSpinBox(my_integer)
        slider = RQSlider(my_integer, Qt.Horizontal)
        dial = RQDial(my_integer)
        progress_bar = RQProgressBar(my_integer)

        layout.addWidget(spinbox)
        layout.addWidget(slider)
        layout.addWidget(dial)
        layout.addWidget(progress_bar)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
