from pyreaqtive import RQFloat, RQComputedFloat
import pytest_cases
from tests.signal_checker import *


@pytest_cases.parametrize("initial", [-5.4, 0.0, 3.6, 1000053.4])
def test_float(initial):
    m = RQFloat(initial)
    connect_signal(m.rq_data_changed)

    assert m._float == initial
    assert m.get() == initial

    assert str(m) == str(initial)
    assert int(m) == int(initial)
    assert float(m) == float(initial)

    m.set(90.5)
    assert_signal_emitted(m.rq_data_changed)

    assert m.get() == 90.5


def test_computed_float():
    m1 = RQFloat(5.5)
    m2 = RQFloat(2)

    mc1 = RQComputedFloat(
        lambda m1, m2: m1 + m2 + 1,
        m1=m1,
        m2=m2
    )
    connect_signal(mc1.rq_data_changed)

    assert float(mc1) == 8.5

    m1.set(1)
    assert_signal_emitted(mc1.rq_data_changed)
    assert float(mc1) == 4
