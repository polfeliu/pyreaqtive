from typing import TYPE_CHECKING, Union, Type, Callable
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel

import pytest_cases

from pyreaqtive import RQWidgetObject, RQObject

from ..qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


class SampleObject:
    def __init__(self, text: str) -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text


class WidgetA(QWidget):

    def __init__(self, obj: SampleObject) -> None:
        super(WidgetA, self).__init__()
        self.obj = obj
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(QLabel(str(obj)))


class WidgetB(QWidget):

    def __init__(self, obj: SampleObject) -> None:
        super(WidgetB, self).__init__()
        self.obj = obj
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(QLabel(str(obj)))


@pytest_cases.parametrize("widget_callback", [True, False])
@pytest_cases.parametrize("layout_type", [QHBoxLayout, QVBoxLayout])
def test_rqwidget(
        widget_callback: bool,
        layout_type: Union[Type[QHBoxLayout], Type[QVBoxLayout]],
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name
) -> None:
    instance_1 = SampleObject("INST1")
    instance_2 = SampleObject("INST2")

    model = RQObject(instance_1)
    layout = layout_type()

    widget: Union[Type[QWidget], Callable[[object], QWidget]]

    if widget_callback:
        def widget(obj: object) -> QWidget:
            if not isinstance(obj, SampleObject):
                raise TypeError

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
    widget_2 = RQWidgetObject(  # pylint: disable=unused-variable
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
