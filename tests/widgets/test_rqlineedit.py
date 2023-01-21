from typing import TYPE_CHECKING, Union

import pytest_cases
import pytest

from PyQt5 import QtCore

from pyreaqtive import RQText, RQComputedText, RQLineEdit

from ..qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("initial_value", ["Hello"])
@pytest_cases.parametrize("reactive", [True, False])
@pytest_cases.parametrize("wait_for_finish", [True, False])
def test_rqdial(
        initial_value: str,
        reactive: bool,
        wait_for_finish: bool,
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name
) -> None:
    model: Union[str, RQText]

    if reactive:
        model = RQText(initial_value)
    else:
        model = initial_value

    widget_1 = RQLineEdit(model, wait_for_finish=wait_for_finish)
    window_fixture.layout().addWidget(widget_1)

    if reactive:
        widget_2 = RQLineEdit(model)
        window_fixture.layout().addWidget(widget_2)

    window_fixture.show()

    assert widget_1.text() == initial_value

    for _ in range(10):
        qtbot.keyClick(widget_1, QtCore.Qt.Key_Backspace)

    qtbot.keyClick(widget_1, QtCore.Qt.Key_A)
    qtbot.keyClick(widget_1, QtCore.Qt.Key_S)
    qtbot.keyClick(widget_1, QtCore.Qt.Key_D)
    qtbot.keyClick(widget_1, QtCore.Qt.Key_F)

    changed_text = "asdf"

    if not wait_for_finish:
        assert widget_1.model.get() == changed_text
    else:
        # Has not changed model
        assert widget_1.model.get() == initial_value
        qtbot.keyClick(widget_1, QtCore.Qt.Key_Enter)
        assert widget_1.text() == changed_text

    if reactive:
        assert widget_2.text() == changed_text
        widget_2.setText("world")
        assert widget_1.text() == "world"
        assert widget_2.text() == "world"


def test_rqdial_readonly(
        qtbot: 'QtBot'  # pylint: disable=unused-argument
) -> None:
    model = RQComputedText(
        lambda: "Lorem"
    )

    with pytest.raises(IOError):
        model = RQLineEdit(model)
