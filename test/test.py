from encodings.punycode import selective_find

from PyQt5.QtWidgets import *
from pyreaqtive import *
import sys

class Counter(QWidget):

    mycounter: RQInt

    def __init__(self):
        super().__init__()

        self.mycounter = RQInt(1)

class CounterWidget(RQWidget):

    model: Counter

    def __init__(self, model: Counter):
        self.model = model
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        self.counter_increment_button = QPushButton("+")
        self.counter_increment_button.clicked.connect(self.increment)
        self.main_layout.addWidget(self.counter_increment_button)
        self.counter_decrement_button = QPushButton("-")
        self.counter_decrement_button.clicked.connect(self.decrement)
        self.main_layout.addWidget(self.counter_decrement_button)

        self.counter_spin_box = RQSpinBox(self.model.mycounter)
        self.main_layout.addWidget(self.counter_spin_box)

        self.counter_display_label = RQLabel(self.model.mycounter)
        self.main_layout.addWidget(self.counter_display_label)

    def increment(self):
        self.model.mycounter.increment()

    def decrement(self):
        self.model.mycounter.decrement()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.counters = RQList([Counter()])

        self.bool_state = RQBool(True)

        self.init_ui()

    def counter_widget_callback(self, model: Counter):
        return CounterWidget(model)

    def init_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.counters_layout = RQVBoxLayout(model=self.counters, widget_callback=self.counter_widget_callback)
        self.main_layout.addLayout(self.counters_layout)

        self.add_counter = QPushButton("Add Counter")
        self.add_counter.clicked.connect(lambda: self.counters.append(Counter()))
        self.main_layout.addWidget(self.add_counter)
        self.remove_counter = QPushButton("Remove Counter")
        self.remove_counter.clicked.connect(lambda: self.counters.pop())
        self.main_layout.addWidget(self.remove_counter)

        self.checkbox_1 = RQCheckbox(self.bool_state, "Checkbox 1")
        self.main_layout.addWidget(self.checkbox_1)
        self.checkbox_2 = RQCheckbox(self.bool_state, "Checkbox 2")
        self.main_layout.addWidget(self.checkbox_2)

        self.show()

app = QApplication(sys.argv)
mainWindow = MainWindow()

sys.exit(app.exec_())
