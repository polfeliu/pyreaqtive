from pyreaqtive import RQWidgetObject, RQObject
import pytest_cases

from qtpy.QtWidgets import *
from ..qtbot_window import window_fixture


class SampleObject:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class WidgetA(QWidget):

    def __init__(self, obj):
        super(WidgetA, self).__init__()
        self.obj = obj
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(QLabel(str(obj)))


class WidgetB(QWidget):

    def __init__(self, obj):
        super(WidgetB, self).__init__()
        self.obj = obj
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

    widget_1 = RQWidgetObject(
        model=model,
        layout=layout,
        widget=widget
    )
    widget_2 = RQWidgetObject(
        model=model,
        layout=layout,
        widget=widget
    )
    main_widget = QWidget()
    window_fixture.layout().addWidget(main_widget)
    main_widget.setLayout(layout)
    window_fixture.show()

    assert layout.itemAt(0).widget().obj == instance_1
    assert layout.itemAt(1).widget().obj == instance_1

    model.set(instance_2)
    assert layout.itemAt(0).widget().obj == instance_2
    assert layout.itemAt(1).widget().obj == instance_2

    widget_1.hide()
    assert layout.itemAt(0).widget().isHidden()
    assert layout.itemAt(1).widget().isHidden()
    widget_1.show()
