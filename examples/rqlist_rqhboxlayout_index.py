import string
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from pyreaqtive.models import RQList, RQModel, RQFormatter
from pyreaqtive.widgets import RQLabel
from pyreaqtive.layouts import RQHBoxLayout

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot


class Item(RQModel):

    def __init__(self):
        super(Item, self).__init__()


next_letter = 0


class ItemWidget(QWidget):

    def __init__(self, model: Item, list_model: RQList):
        super().__init__()

        self.model = model
        self.list_model = list_model

        self.main_layout = QVBoxLayout(self)
        self.resize(200,200)

        global next_letter
        self.letter_label = QLabel(
            string.ascii_uppercase[next_letter]
        )
        next_letter += 1
        self.main_layout.addWidget(self.letter_label)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(
            lambda: self.model.__delete__()
        )
        self.main_layout.addWidget(self.delete_button)

        # Get a reactive index of the item in the list
        self.index = list_model.reactive_index(model)
        self.index_label = RQLabel(
            RQFormatter(
                "index: {index}",
                index=self.index
            )
        )
        self.main_layout.addWidget(self.index_label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.my_list = RQList()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        item_display = RQHBoxLayout(
            model=self.my_list,
            widget=ItemWidget
        )
        layout.addLayout(item_display)

    @pyqtSlot()
    def add_item(self):
        self.my_list.append(
            Item()
        )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
