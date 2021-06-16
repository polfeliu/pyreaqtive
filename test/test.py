from PyQt5.QtWidgets import *
from pyreaqtive import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.counter_add_push_button = QPushButton("add")
        self.main_layout.addWidget(self.counter_add_push_button)
        self.counter_display_label = RQLabel("1")
        self.main_layout.addWidget(self.counter_display_label)

        self.show()


app = QApplication(sys.argv)
mainWindow = MainWindow()


sys.exit(app.exec_())