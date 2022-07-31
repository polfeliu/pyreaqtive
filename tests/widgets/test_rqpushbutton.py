from pyreaqtive import RQPushButton, RQText
import pytest_cases

from ..qtbot_window import window_fixture


@pytest_cases.parametrize("initial_value", ["Hello", "World"])
def test_rqcheckbox_rqbool(initial_value, qtbot, window_fixture):
    text = RQText(initial_value)

    button = RQPushButton(text)

    window_fixture.layout().addWidget(button)
    window_fixture.show()

    assert button.text() == initial_value

    text.set("Goodbye")
    assert button.text() == "Goodbye"
