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
        label = RQLabel(
            RQComputedText(
                "entered text is: {text}",
                text=my_text
            )
        )

        layout.addWidget(line_edit)
        layout.addWidget(label)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
