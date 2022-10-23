from typing import TYPE_CHECKING

import pytest_cases

from pyreaqtive import RQPushButton, RQText

from ..qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("initial_value", ["Hello", "World"])
def test_rqcheckbox_rqbool(
        initial_value: str,
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name
) -> None:
    text = RQText(initial_value)

    button = RQPushButton(text)

    window_fixture.layout().addWidget(button)
    window_fixture.show()

    assert button.text() == initial_value

    text.set("Goodbye")
    assert button.text() == "Goodbye"
