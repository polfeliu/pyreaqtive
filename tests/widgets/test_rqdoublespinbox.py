from typing import TYPE_CHECKING, Union

import pytest_cases
import pytest

from PyQt5 import QtCore

from pyreaqtive import RQFloat, RQComputedFloat, RQDoubleSpinBox

from ..qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("initial_value", [
    2.2,
    7.3,
    1007.4,
    -6.6
])
@pytest_cases.parametrize("reactive", [True, False])
@pytest_cases.parametrize("wait_for_finish", [True, False])
def test_rqdoublespinbox(
        initial_value: float,
        reactive: bool,
        wait_for_finish: bool,
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name
) -> None:
    model: Union[float, RQFloat]

    if reactive:
        model = RQFloat(initial_value)
    else:
        model = initial_value

    saturated_initial_value = min(max(0, initial_value), 99.99)

    widget_1 = RQDoubleSpinBox(model, wait_for_finish=wait_for_finish)
    window_fixture.layout().addWidget(widget_1)

    if reactive:
        widget_2 = RQDoubleSpinBox(model)
        window_fixture.layout().addWidget(widget_2)

    window_fixture.show()

    assert widget_1.value() == saturated_initial_value

    for _ in range(10):
        qtbot.keyClick(widget_1, QtCore.Qt.Key_Delete)
    qtbot.keyClick(widget_1, QtCore.Qt.Key_5)
    # comma or period as decimal separator depending on the platform, other is ignored
    qtbot.keyClick(widget_1, QtCore.Qt.Key_Comma)
    qtbot.keyClick(widget_1, QtCore.Qt.Key_Period)
    qtbot.keyClick(widget_1, QtCore.Qt.Key_4)

    if not wait_for_finish:
        assert widget_1.model.get() == 5.4
    else:
        # Has not changed model
        assert widget_1.model.get() == initial_value
        qtbot.keyClick(widget_1, QtCore.Qt.Key_Enter)
        assert widget_1.value() == 5.4

    if reactive:
        assert widget_2.value() == 5.4
        widget_2.setValue(30)
        assert widget_1.value() == 30
        assert widget_2.value() == 30


def test_rqdial_readonly(
        qtbot: 'QtBot'  # pylint: disable=unused-argument
) -> None:
    model = RQComputedFloat(
        lambda: 1
    )

    with pytest.raises(IOError):
        model = RQDoubleSpinBox(model)
