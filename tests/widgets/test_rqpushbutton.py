from typing import TYPE_CHECKING, Union

from pyreaqtive import RQPushButton, RQText
import pytest_cases

from ..qtbot_window import window_fixture

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("initial_value", ["Hello", "World"])
def test_rqcheckbox_rqbool(initial_value: str, qtbot: 'QtBot', window_fixture: 'QMainWindow') -> None:
    text = RQText(initial_value)

    button = RQPushButton(text)

    window_fixture.layout().addWidget(button)
    window_fixture.show()

    assert button.text() == initial_value

    text.set("Goodbye")
    assert button.text() == "Goodbye"
