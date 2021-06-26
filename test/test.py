from PyQt5.QtWidgets import *
from pyreaqtive import *
import sys
import random

from typing import Type


class Counter(RQModel):
    mycounter: RQInt
    rq_list_index: RQInt

    def __init__(self):
        super().__init__()

        self.mycounter = RQInt(10)
        self.rq_list_index = RQInt(0)


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

        self.counter_display_label = RQLabel(
            RQFormatter(
                "count x2 {countx2}, index: {index}",
                countx2=RQFunction(
                    lambda count: count * 2,
                    count=self.model.mycounter
                ),
                index=self.model.rq_list_index
            )
        )
        self.main_layout.addWidget(self.counter_display_label)

        self.model.mycounter._rq_data_changed.connect(self.update_counter_text_size)

        self.update_counter_text_size()

    # example of a custom function binding
    def update_counter_text_size(self):
        f = self.counter_display_label.font()
        f.setPointSize(self.model.mycounter)
        self.counter_display_label.setFont(f)

    def increment(self):
        self.model.mycounter.increment()

    def decrement(self):
        self.model.mycounter.decrement()


class AlternateCounterWidget(RQWidget):

    def __init__(self, model: Counter):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(
            QPushButton("Alternate Counter Widget")
        )

        self.main_layout.addWidget(
            RQLabel(
                RQFormatter(
                    "index is {index}",
                    index=model.rq_list_index
                )
            )
        )

class ChoiceOption(RQModel):

    name: str

    def __str__(self):
        return self.name



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.counters = RQList([Counter])
        self.bool_state = RQBool(True)
        self.text_1 = RQText("hello!")

        self.choice_list = RQList()
        self.choice_list.append(ChoiceOption).name = "option 1"
        self.choice_list.append(ChoiceOption).name = "option 2"
        self.choice_list.append(ChoiceOption).name = "option 3"
        self.choice = RQChoice(self.choice_list)
        self.init_ui()

    def counter_widget_callback(self, model: Type[RQModel]) -> Type[QWidget]:
        if random.choice([True, False]):
            return CounterWidget(model)
        else:
            return AlternateCounterWidget(model)

    def init_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.counters_layout = RQVBoxLayout(model=self.counters, widget_callback=self.counter_widget_callback)
        self.main_layout.addLayout(self.counters_layout)

        self.add_counter = QPushButton("Add Counter")
        self.add_counter.clicked.connect(lambda: self.counters.append(Counter))
        self.main_layout.addWidget(self.add_counter)
        self.remove_counter = QPushButton("Remove Counter")
        self.remove_counter.clicked.connect(lambda: self.counters.pop())
        self.main_layout.addWidget(self.remove_counter)

        self.checkbox_1 = RQCheckbox(self.bool_state, "Checkbox 1")
        self.main_layout.addWidget(self.checkbox_1)
        self.checkbox_2 = RQCheckbox(self.bool_state, "Checkbox 2")
        self.main_layout.addWidget(self.checkbox_2)

        self.line_edit = RQLineEdit(self.text_1)
        self.main_layout.addWidget(self.line_edit)
        self.label_text_1 = RQLabel(RQFormatter("text {text_1}", text_1=self.text_1))
        self.main_layout.addWidget(self.label_text_1)

        self.combobox_1 = RQCombobox(self.choice)
        self.main_layout.addWidget(self.combobox_1)
        self.combobox_2 = RQCombobox(self.choice)
        self.main_layout.addWidget(self.combobox_2)

        self.show()


app = QApplication(sys.argv)
mainWindow = MainWindow()

sys.exit(app.exec_())
