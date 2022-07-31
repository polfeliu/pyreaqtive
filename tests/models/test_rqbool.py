from pyreaqtive import RQBool, RQComputedBool
import pytest_cases
from tests.signal_checker import *


def assert_bool_state(m, state):
    assert m._bool == state
    assert m.get() == state
    assert bool(m) == state

    if state:
        assert str(m) == "True"
    else:
        assert str(m) == "False"


@pytest_cases.parametrize("initial_state", [True, False])
def test_bool(initial_state):
    m = RQBool(initial_state)
    connect_signal(m.rq_data_changed)

    assert_bool_state(m, initial_state)

    m.set(initial_state)
    assert_signal_emitted(m.rq_data_changed)
    assert_bool_state(m, initial_state)

    m.set(not initial_state)
    assert_signal_emitted(m.rq_data_changed)
    assert_bool_state(m, not initial_state)

    m.toggle()
    assert_signal_emitted(m.rq_data_changed)
    assert_bool_state(m, initial_state)


def test_computed_bool():
    m1 = RQBool(True)
    m2 = RQBool(True)

    mc = RQComputedBool(
        lambda m1, m2: m1 and m2,
        m1=m1,
        m2=m2
    )

    assert mc.get() is True

    m1.set(False)

    assert mc.get() is False

    m2.set(False)

    assert mc.get() is False

    m1.set(True)
    m2.set(True)

    assert mc.get() is True
