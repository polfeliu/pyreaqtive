from pyreaqtive import RQText, RQComputedText, RQLineEdit
import pytest_cases
import pytest
from PyQt5 import QtCore

from ..qtbot_window import window_fixture


@pytest_cases.parametrize("initial_value", ["Hello"])
@pytest_cases.parametrize("reactive", [True, False])
@pytest_cases.parametrize("wait_for_finish", [True, False])
def test_rqdial(initial_value, reactive, wait_for_finish, qtbot, window_fixture):
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

    for i in range(10):
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


def test_rqdial_readonly(qtbot):
    m = RQComputedText(
        lambda: "Lorem"
    )

    with pytest.raises(IOError):
        m = RQLineEdit(m)
