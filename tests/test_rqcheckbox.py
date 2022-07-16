from pyreaqtive.models import RQBool
from pyreaqtive.widgets import RQCheckBox
import pytest_cases


@pytest_cases.parametrize("initial_state", [True, False])
def test_rqbool(initial_state):
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


def test_rqcomputedbool():
    pass  # state_1 = RQBool(False)
