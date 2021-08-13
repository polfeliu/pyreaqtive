import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, \
    QInputDialog
from pyreaqtive.models import RQList, RQModel, RQChoice
from pyreaqtive.widgets import RQVBoxLayout, RQCombobox

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
import random


# Declare a model for each type
class Fruit(RQModel):

    def __init__(self, name: str):
        super(Fruit, self).__init__()
        self.name = name

    def __str__(self) -> str:
        return self.name


class Grain(RQModel):

    def __init__(self, name: str):
        super(Grain, self).__init__()
        self.name = name

    def __str__(self) -> str:
        return self.name


# Declare a widget for each type
class FruitWidget(QWidget):

    def __init__(self, model: Fruit, list_model: RQList):
        super().__init__()

        # Store the model of the fruit
        self.model = model

        # And the list is present on
        self.list_model = list_model

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(
            QLabel(str(model))  # Simple widget to display the name of the fruit. Could also be reactive!
        )

        # Button to remove itself from the list
        self.remove_button = QPushButton("remove")
        self.remove_button.clicked.connect(self.remove)
        self.main_layout.addWidget(self.remove_button)

    @pyqtSlot()
    def remove(self) -> None:
        # Request that the list removes the model this widget is representing
        self.list_model.remove(self.model)


class GrainWidget(QWidget):

    def __init__(self, model: Fruit, list_model: RQList):
        super().__init__()

        # Store the model of the fruit
        self.model = model

        # And the list is present on
        self.list_model = list_model

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(
            QLabel(str(model))  # Simple widget to display the name of the fruit. Could also be reactive!
        )

        # Button to remove itself from the list
        self.remove_button = QPushButton("remove")
        self.remove_button.clicked.connect(self.remove)
        self.main_layout.addWidget(self.remove_button)

    @pyqtSlot()
    def remove(self) -> None:
        # Request that the list removes the model this widget is representing
        self.list_model.remove(self.model)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Declare the list
        self.fruits_list = RQList()
        self.grains_list = RQList()

        self.my_shopping_list = RQList()

        self.add_fruit_button = QPushButton("Add Fruit")
        self.add_fruit_button.clicked.connect(self.add_fruit)
        layout.addWidget(self.add_fruit_button)

        self.add_grain_button = QPushButton("Add Grain")
        self.add_grain_button.clicked.connect(self.add_grain)
        layout.addWidget(self.add_grain_button)

        self.clear_all_button = QPushButton("Clear")
        self.clear_all_button.clicked.connect(
            lambda: self.fruits_list.clear()
        )
        layout.addWidget(self.clear_all_button)

        # Fruits
        layout.addWidget(QLabel("Fruits"))
        fruits_display = RQVBoxLayout(
            model=self.fruits_list,
            widget=FruitWidget
        )
        layout.addLayout(fruits_display)

        # Grains
        layout.addWidget(QLabel("Grains"))
        grains_display = RQVBoxLayout(
            model=self.grains_list,
            widget=GrainWidget
        )
        layout.addLayout(grains_display)

        # Shopping List
        layout.addWidget(QLabel("Shopping list"))
        grains_display = RQVBoxLayout(
            model=self.grains_list,
            widget=GrainWidget
        )
        layout.addLayout(grains_display)

    @pyqtSlot()
    def add_fruit(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter fruit name:')

        if ok:
            self.fruits_list.append(
                Fruit(text)
            )

    def add_grain(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter grain name:')

        if ok:
            self.grains_list.append(
                Grain(text)
            )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
