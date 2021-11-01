import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyreaqtive.models import RQText
from pyreaqtive.widgets import RQLineEdit, RQLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Declare a text
        my_text = RQText("hello world!")

        # Create a pair of the line edit widgets
        edit_1 = RQLineEdit(my_text)
        edit_2 = RQLineEdit(my_text)

        # Create a label widget
        label = RQLabel(my_text)

        # Add the widgets to the layout
        layout.addWidget(edit_1)
        layout.addWidget(edit_2)
        layout.addWidget(label)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
