from typing import TYPE_CHECKING, Union

import pytest_cases
import pytest

from PyQt5 import QtCore
from pyreaqtive import RQInt, RQComputedInt, RQSpinBox

from ..qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("initial_value", [
    2,
    1007,
    -6
])
@pytest_cases.parametrize("reactive", [True, False])
@pytest_cases.parametrize("wait_for_finish", [True, False])
def test_rqdial(
        initial_value: int,
        reactive: bool,
        wait_for_finish: bool,
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name
) -> None:
    model: Union[RQInt, int]

    if reactive:
        model = RQInt(initial_value)
    else:
        model = initial_value

    saturated_initial_value = min(max(0, initial_value), 99)

    widget_1 = RQSpinBox(model, wait_for_finish=wait_for_finish)
    window_fixture.layout().addWidget(widget_1)

    if reactive:
        widget_2 = RQSpinBox(model)
        window_fixture.layout().addWidget(widget_2)

    window_fixture.show()

    assert widget_1.value() == saturated_initial_value

    qtbot.keyClick(widget_1, QtCore.Qt.Key_Delete)
    qtbot.keyClick(widget_1, QtCore.Qt.Key_Delete)
    qtbot.keyClick(widget_1, QtCore.Qt.Key_5)

    if not wait_for_finish:
        assert widget_1.model.get() == 5
    else:
        # Has not changed model
        assert widget_1.model.get() == initial_value
        qtbot.keyClick(widget_1, QtCore.Qt.Key_Enter)
        assert widget_1.value() == 5

    if reactive:
        assert widget_2.value() == 5
        widget_2.setValue(30)
        assert widget_1.value() == 30
        assert widget_2.value() == 30


def test_rqdial_readonly(
        qtbot: 'QtBot'  # pylint: disable=unused-argument
) -> None:
    model = RQComputedInt(
        lambda: 1
    )

    with pytest.raises(IOError):
        model = RQSpinBox(model)
