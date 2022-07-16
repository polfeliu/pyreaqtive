from pyreaqtive import RQBool
import pytest_cases


def assert_bool_state(m, state):
    assert m._bool == state
    assert m.get() == state
    assert bool(m) == state

    if state:
        assert str(state) == "True"
    else:
        assert str(state) == "False"


@pytest_cases.parametrize("initial_state", [True, False])
def test_bool(initial_state):
    m = RQBool(initial_state)

    assert_bool_state(m, initial_state)

    m.set(initial_state)
    assert_bool_state(m, initial_state)

    m.set(not initial_state)
    assert_bool_state(m, not initial_state)

    m.toggle()
    assert_bool_state(m, initial_state)
