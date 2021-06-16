from PyQt5.QtWidgets import *
from pyreaqtive import *
import sys

"""class MyCounter(RQModel):

    count = RQInt(1)"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mycounter = RQInt(1)

        self.init_ui()

    def init_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.counter_increment_button = QPushButton("+")
        self.counter_increment_button.clicked.connect(lambda: self.mycounter.increment())
        self.main_layout.addWidget(self.counter_increment_button)
        self.counter_decrement_button = QPushButton("-")
        self.counter_decrement_button.clicked.connect(lambda: self.mycounter.decrement())
        self.main_layout.addWidget(self.counter_decrement_button)
        self.counter_display_label = RQLabel(self.mycounter)
        self.main_layout.addWidget(self.counter_display_label)

        self.show()

app = QApplication(sys.argv)
mainWindow = MainWindow()

sys.exit(app.exec_())