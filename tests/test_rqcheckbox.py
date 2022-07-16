from pyreaqtive.models import RQBool
from pyreaqtive.widgets import RQCheckBox


def test_rqbool(qtbot):
    state = RQBool(False)

    checkbox_1 = RQCheckBox(state, "checkbox 1")
    checkbox_2 = RQCheckBox(state, "checkbox 2")

    # Initial state of the model is set to false
    assert state.get() == False

    assert checkbox_1.isChecked() == False
    assert checkbox_2.isChecked() == False

    # Toggle with checkbox 1
    checkbox_1.click()
    assert checkbox_1.isChecked() == True
    assert state.get() == True
    assert checkbox_2.isChecked() == True

    # Toggle with checkbox 2
    checkbox_2.click()
    assert checkbox_2.isChecked() == False
    assert state.get() == False
    assert checkbox_1.isChecked() == False
