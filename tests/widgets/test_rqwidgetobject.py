from pyreaqtive import RQWidgetObject, RQObject
import pytest_cases

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .qtbot_window import window_fixture
from time import sleep


class SampleObject:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class WidgetA(QWidget):

    def __init__(self, obj):
        super(WidgetA, self).__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(QLabel(str(obj)))


class WidgetB(QWidget):

    def __init__(self, obj):
        super(WidgetB, self).__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(QLabel(str(obj)))


@pytest_cases.parametrize("widget_callback", [True, False])
@pytest_cases.parametrize("layout", [QHBoxLayout, QVBoxLayout])
def test_rqwidget(widget_callback, layout, qtbot, window_fixture):
    instance_1 = SampleObject("INST1")
    instance_2 = SampleObject("INST2")

    model = RQObject(instance_1)
    layout = layout()
    if widget_callback:
        def widget(obj):
            if obj == instance_1:
                return WidgetA(obj)
            elif obj == instance_2:
                return WidgetB(obj)
            else:
                raise ValueError
    else:
        widget = WidgetB

    widget = RQWidgetObject(
        model=model,
        layout=layout,
        widget=widget
    )
    main_widget = QWidget()
    window_fixture.layout().addWidget(main_widget)
    main_widget.setLayout(layout)
    window_fixture.show()
    model.set(instance_2)
