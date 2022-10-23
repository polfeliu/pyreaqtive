import pytest_cases
from tests.signal_checker import connect_signal, assert_signal_emitted

from pyreaqtive import RQBool, RQComputedBool


def assert_bool_state(model: RQBool, state: bool) -> None:
    assert model._bool == state  # pylint: disable=protected-access
    assert model.get() == state
    assert bool(model) == state

    if state:
        assert str(model) == "True"
    else:
        assert str(model) == "False"


@pytest_cases.parametrize("initial_state", [True, False])
def test_bool(initial_state: bool) -> None:
    model = RQBool(initial_state)
    connect_signal(model.rq_data_changed)

    assert_bool_state(model, initial_state)

    model.set(initial_state)
    assert_signal_emitted(model.rq_data_changed)
    assert_bool_state(model, initial_state)

    model.set(not initial_state)
    assert_signal_emitted(model.rq_data_changed)
    assert_bool_state(model, not initial_state)

    model.toggle()
    assert_signal_emitted(model.rq_data_changed)
    assert_bool_state(model, initial_state)


def test_computed_bool() -> None:
    model1 = RQBool(True)
    model2 = RQBool(True)

    model_computed = RQComputedBool(
        lambda m1, m2: m1 and m2,
        m1=model1,
        m2=model2
    )

    assert model_computed.get() is True

    model1.set(False)

    assert model_computed.get() is False

    model2.set(False)

    assert model_computed.get() is False

    model1.set(True)
    model2.set(True)

    assert model_computed.get() is True
