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

        self.counter_add_push_button = QPushButton("add")
        self.counter_add_push_button.clicked.connect(self.add_to_counter)
        self.main_layout.addWidget(self.counter_add_push_button)
        self.counter_display_label = RQLabel(self.mycounter)
        self.main_layout.addWidget(self.counter_display_label)

        self.show()

    def add_to_counter(self):
        self.mycounter.set(self.mycounter.get() + 1)

app = QApplication(sys.argv)
mainWindow = MainWindow()

sys.exit(app.exec_())