from pyreaqtive import RQInt, RQComputedInt
import pytest_cases
from tests.signal_checker import *


@pytest_cases.parametrize("initial", [-4, 0, 8, 23323])
def test_int(initial):
    m = RQInt(initial)
    connect_signal(m.rq_data_changed)

    assert m._int == initial
    assert m.get() == initial

    assert str(m) == str(initial)
    assert int(m) == int(initial)
    assert float(m) == float(initial)

    m.set(90)
    assert_signal_emitted(m.rq_data_changed)

    assert m.get() == 90

    m.increment()
    assert_signal_emitted(m.rq_data_changed)
    assert m.get() == 91
    m.decrement()
    assert_signal_emitted(m.rq_data_changed)
    assert m.get() == 90

    m.increment(10)
    assert_signal_emitted(m.rq_data_changed)
    assert m.get() == 100
    m.decrement(5)
    assert_signal_emitted(m.rq_data_changed)
    assert m.get() == 95


def test_computed_int():
    m1 = RQInt(2)
    m2 = RQInt(5)

    mc1 = RQComputedInt(
        lambda m1, m2: m1 * m2,
        m1=m1,
        m2=m2
    )
    connect_signal(mc1.rq_data_changed)

    mc2 = RQComputedInt(
        lambda m2, mc1: m2 + mc1,
        m2=m2,
        mc1=mc1
    )
    connect_signal(mc2.rq_data_changed)

    assert int(mc1) == 10
    assert int(mc2) == 15

    m1.set(10)
    assert_signal_emitted(mc1.rq_data_changed)
    assert_signal_emitted(mc2.rq_data_changed)
    assert int(mc1) == 50
    assert int(mc2) == 55
