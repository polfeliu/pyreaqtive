import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from pyreaqtive.models import RQText, RQComputedText
from pyreaqtive.widgets import RQLineEdit, RQLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        my_text = RQText("hello")

        line_edit = RQLineEdit(my_text)

        # Text expression can be in format style
        label_1 = RQLabel(
            RQComputedText(
                "entered text is: {text}",
                text=my_text
            )
        )

        # Or as a lambda expression
        label_2 = RQLabel(
            RQComputedText(
                lambda text: f"entered text is: {text}",
                text=my_text
            )
        )

        layout.addWidget(line_edit)
        layout.addWidget(label_1)
        layout.addWidget(label_2)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
