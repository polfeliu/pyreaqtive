import pytest_cases
from tests.signal_checker import connect_signal, assert_signal_emitted

from pyreaqtive import RQInt, RQComputedInt


@pytest_cases.parametrize("initial", [-4, 0, 8, 23323])
def test_int(initial: int) -> None:
    model = RQInt(initial)
    connect_signal(model.rq_data_changed)

    assert model._int == initial  # pylint: disable=protected-access
    assert model.get() == initial

    assert str(model) == str(initial)
    assert int(model) == int(initial)
    assert float(model) == float(initial)

    model.set(90)
    assert_signal_emitted(model.rq_data_changed)

    assert model.get() == 90

    model.increment()
    assert_signal_emitted(model.rq_data_changed)
    assert model.get() == 91
    model.decrement()
    assert_signal_emitted(model.rq_data_changed)
    assert model.get() == 90

    model.increment(10)
    assert_signal_emitted(model.rq_data_changed)
    assert model.get() == 100
    model.decrement(5)
    assert_signal_emitted(model.rq_data_changed)
    assert model.get() == 95


def test_computed_int() -> None:
    model1 = RQInt(2)
    model2 = RQInt(5)

    mc1 = RQComputedInt(
        lambda m1, m2: m1 * m2,
        m1=model1,
        m2=model2
    )
    connect_signal(mc1.rq_data_changed)

    mc2 = RQComputedInt(
        lambda m2, mc1: m2 + mc1,
        m2=model2,
        mc1=mc1
    )
    connect_signal(mc2.rq_data_changed)

    assert int(mc1) == 10
    assert int(mc2) == 15

    model1.set(10)
    assert_signal_emitted(mc1.rq_data_changed)
    assert_signal_emitted(mc2.rq_data_changed)
    assert int(mc1) == 50
    assert int(mc2) == 55
