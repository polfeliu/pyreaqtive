import pytest

from pyreaqtive import RQModel, RQComputedModel, RQInt
from .signal_checker import *


def test_model():
    m = RQModel()
    connect_signal(m.rq_data_changed)
    connect_signal(m._rq_delete)

    with pytest.raises(NotImplementedError):
        m.get()

    with pytest.raises(NotImplementedError):
        m.set(1)

    m.rq_data_changed.emit()
    assert_signal_emitted(m.rq_data_changed)

    m.__delete__()
    assert_signal_emitted(m._rq_delete)


def test_reactive_model():
    m1 = RQInt(2)
    m2 = RQInt(5)
    m3 = 10

    def callback(m1, m2):
        return m1 * m2

    with pytest.raises(TypeError):
        RQComputedModel(lambda: None)

    class TestRQModel(RQComputedModel, RQInt):
        def __init__(self, function, **kwargs: RQModel):
            RQInt.__init__(self, 0)
            RQComputedModel.__init__(self, function, **kwargs)

    mc = TestRQModel(
        callback,
        m1=m1,
        m2=m2
    )

    assert mc.rq_read_only == True
    assert mc.rq_computed_function == callback
    assert mc.rq_computed_variables['m1'] == m1
    assert mc.rq_computed_variables['m2'] == m2

    assert mc.get() == 10

    with pytest.raises(RuntimeError):
        mc.set(1)

    m1.set(1)
    assert mc.get() == 5

    m1.set(10)
    m2.set(10)
    assert mc.get() == 100
