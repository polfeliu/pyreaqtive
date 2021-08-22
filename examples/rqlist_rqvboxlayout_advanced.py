import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, \
    QInputDialog
from pyreaqtive.models import RQList, RQModel
from pyreaqtive.layouts import RQVBoxLayout

from PyQt5.QtCore import pyqtSlot


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

    def __init__(self, model: Fruit, list_model: RQList, shopping_list: RQList):
        super().__init__()

        # Store the model of the fruit
        self.model = model

        # And the list is present on
        self.list_model = list_model

        # And the shopping list for the button
        self.shopping_list = shopping_list

        self.main_layout = QHBoxLayout(self)
        text = str(model)
        if list_model == shopping_list:
            text = "Fruit " + text
        self.main_layout.addWidget(QLabel(text))

        if list_model == shopping_list:
            self.remove_button = QPushButton("remove")
            self.remove_button.clicked.connect(self.remove_from_shopping_list)
            self.main_layout.addWidget(self.remove_button)

        if list_model != shopping_list:
            self.delete_button = QPushButton("delete")
            self.delete_button.clicked.connect(self.delete_model)
            self.main_layout.addWidget(self.delete_button)

            self.add_shopping_button = QPushButton("add to shopping list")
            self.add_shopping_button.clicked.connect(self.add_to_shopping_list)
            self.main_layout.addWidget(self.add_shopping_button)

    @pyqtSlot()
    def delete_model(self) -> None:
        # Delete the model, is removed from all lists
        self.model.__delete__()

    @pyqtSlot()
    def remove_from_shopping_list(self) -> None:
        # Remove model from the shopping list
        self.list_model.remove(self.model)

    @pyqtSlot()
    def add_to_shopping_list(self):
        self.shopping_list.append(self.model)


class GrainWidget(QWidget):

    def __init__(self, model: Grain, list_model: RQList, shopping_list: RQList):
        super().__init__()

        self.model = model
        self.list_model = list_model
        self.shopping_list = shopping_list

        self.main_layout = QHBoxLayout(self)
        text = str(model)
        if list_model == shopping_list:
            text = "Grain " + text
        self.main_layout.addWidget(QLabel(text))

        if list_model == shopping_list:
            self.remove_button = QPushButton("remove")
            self.remove_button.clicked.connect(self.remove_from_shopping_list)
            self.main_layout.addWidget(self.remove_button)

        if list_model != shopping_list:
            self.delete_button = QPushButton("delete")
            self.delete_button.clicked.connect(self.delete_model)
            self.main_layout.addWidget(self.delete_button)

            self.add_shopping_button = QPushButton("add to shopping list")
            self.add_shopping_button.clicked.connect(self.add_to_shopping_list)
            self.main_layout.addWidget(self.add_shopping_button)

    @pyqtSlot()
    def delete_model(self) -> None:
        self.model.__delete__()

    @pyqtSlot()
    def remove_from_shopping_list(self) -> None:
        self.list_model.remove(self.model)

    @pyqtSlot()
    def add_to_shopping_list(self):
        self.shopping_list.append(self.model)


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

        self.shopping_list = RQList()

        self.add_fruit_button = QPushButton("Add Fruit")
        self.add_fruit_button.clicked.connect(self.add_fruit)
        layout.addWidget(self.add_fruit_button)

        self.add_grain_button = QPushButton("Add Grain")
        self.add_grain_button.clicked.connect(self.add_grain)
        layout.addWidget(self.add_grain_button)

        # Fruits
        layout.addWidget(QLabel("Fruits"))
        fruits_display = RQVBoxLayout(
            model=self.fruits_list,

            # To pass additional parameters to new widget, place a function that controls the instantiation
            widget=lambda item_model, list_model: FruitWidget(item_model, list_model, self.shopping_list)
        )
        layout.addLayout(fruits_display)

        # Grains
        layout.addWidget(QLabel("Grains"))
        grains_display = RQVBoxLayout(
            model=self.grains_list,
            widget=lambda item_model, list_model: GrainWidget(item_model, list_model, self.shopping_list)
        )
        layout.addLayout(grains_display)

        # Shopping List
        layout.addWidget(QLabel("Shopping list"))
        shopping_display = RQVBoxLayout(
            model=self.shopping_list,
            widget=self.new_shopping_item
        )
        layout.addLayout(shopping_display)

    def new_shopping_item(self, item_model: RQModel, list_model: RQList) -> QWidget:
        if isinstance(item_model, Fruit):
            return FruitWidget(item_model, list_model, self.shopping_list)
        elif isinstance(item_model, Grain):
            return GrainWidget(item_model, list_model, self.shopping_list)
        else:
            raise TypeError

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
