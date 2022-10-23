from typing import TYPE_CHECKING

from pyreaqtive import RQBool, RQComputedBool, RQCheckBox
import pytest_cases
import pytest

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("initial_state", [True, False])
def test_rqcheckbox_rqbool(initial_state: bool, qtbot: 'QtBot') -> None:
    state = RQBool(initial_state)

    checkbox_1 = RQCheckBox(state, "checkbox 1")
    checkbox_2 = RQCheckBox(state, "checkbox 2")

    # Initial state of the model is set to initial state
    assert state.get() == initial_state
    assert checkbox_1.isChecked() == initial_state
    assert checkbox_2.isChecked() == initial_state

    # Toggle with checkbox 1
    checkbox_1.click()
    assert checkbox_1.isChecked() == (not initial_state)
    assert state.get() == (not initial_state)
    assert checkbox_2.isChecked() == (not initial_state)

    # Toggle with checkbox 2
    checkbox_2.click()
    assert checkbox_2.isChecked() == initial_state
    assert state.get() == initial_state
    assert checkbox_1.isChecked() == initial_state

    state.toggle()
    assert state.get() == (not initial_state)
    assert checkbox_1.isChecked() == (not initial_state)
    assert checkbox_2.isChecked() == (not initial_state)


@pytest_cases.parametrize("initial_state", [True, False])
def test_rqcheckbox_non_reactive(initial_state: bool, qtbot: 'QtBot') -> None:
    checkbox = RQCheckBox(initial_state)
    assert isinstance(checkbox.model, RQBool)
    assert checkbox.isChecked() == initial_state


def test_checkbox_readonly() -> None:
    m = RQComputedBool(
        lambda: True
    )

    with pytest.raises(IOError):
        RQCheckBox(m)
