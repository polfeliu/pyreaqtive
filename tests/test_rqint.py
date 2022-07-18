from pyreaqtive import RQInt, RQComputedInt
import pytest_cases


@pytest_cases.parametrize("initial", [-4, 0, 8, 23323])
def test_int(initial):
    m = RQInt(initial)
    assert m._int == initial
    assert m.get() == initial

    assert str(m) == str(initial)
    assert int(m) == int(initial)

    m.set(90)

    assert m.get() == 90

    m.increment()
    assert m.get() == 91
    m.decrement()
    assert m.get() == 90

    m.increment(10)
    assert m.get() == 100
    m.decrement(5)
    assert m.get() == 95

def test_computed_int():
    m1 = RQInt(2)
    m2 = RQInt(5)

    mc1 = RQComputedInt(
        lambda m1, m2: m1 * m2,
        m1=m1,
        m2=m2
    )

    mc2 = RQComputedInt(
        lambda m2, mc1: m2 + mc1,
        m2=m2,
        mc1=mc1
    )

    assert int(mc1) == 10
    assert int(mc2) == 15

    m1.set(10)
    assert int(mc1) == 50
    assert int(mc2) == 55
