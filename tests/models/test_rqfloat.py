import pytest_cases
from tests.signal_checker import connect_signal, assert_signal_emitted

from pyreaqtive import RQFloat, RQComputedFloat


@pytest_cases.parametrize("initial", [-5.4, 0.0, 3.6, 1000053.4])
def test_float(initial: float) -> None:
    model = RQFloat(initial)
    connect_signal(model.rq_data_changed)

    assert model._float == initial  # pylint: disable=protected-access
    assert model.get() == initial

    assert str(model) == str(initial)
    assert int(model) == int(initial)
    assert float(model) == float(initial)

    model.set(90.5)
    assert_signal_emitted(model.rq_data_changed)

    assert model.get() == 90.5


def test_computed_float() -> None:
    model1 = RQFloat(5.5)
    model2 = RQFloat(2)

    mc1 = RQComputedFloat(
        lambda m1, m2: m1 + m2 + 1,
        m1=model1,
        m2=model2
    )
    connect_signal(mc1.rq_data_changed)

    assert float(mc1) == 8.5

    model1.set(1)
    assert_signal_emitted(mc1.rq_data_changed)
    assert float(mc1) == 4
