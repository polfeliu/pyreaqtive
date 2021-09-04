import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel

from pyreaqtive.models import RQBool, RQObject
from pyreaqtive.widgets import RQWidgetObject


class TypeA:
    attribute_a = 'hello'


class TypeB:
    attribute_b = 'goodbye'


class WidgetA(QWidget):

    def __init__(self):
        super(WidgetA, self).__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(QLabel("A"))


class WidgetB(QWidget):

    def __init__(self):
        super(WidgetB, self).__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(QLabel("B"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        change_button = QPushButton("change my_object")
        change_button.clicked.connect(self.toggle_object_to_display)
        layout.addWidget(change_button)

        self.object_a = TypeA()
        self.object_b = TypeB()

        self.object_to_display = RQObject(self.object_a)
        widget = RQWidgetObject(self.object_to_display, layout, widget=self.choose_widget)

    def choose_widget(self, object):
        if isinstance(object, TypeA):
            return WidgetA()
        if isinstance(object, TypeB):
            return WidgetB()

    def toggle_object_to_display(self):
        if isinstance(self.object_to_display.get(), TypeA):
            print("b")
            self.object_to_display.set(self.object_b)
        elif isinstance(self.object_to_display.get(), TypeB):
            print("a")
            self.object_to_display.set(self.object_a)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
