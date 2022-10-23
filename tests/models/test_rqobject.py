import pytest
from tests.signal_checker import *

from pyreaqtive import RQObject


def test_object() -> None:
    class Sample:
        pass

    class DunderSamples:
        def __str__(self) -> str:
            return "Hello"

        def __int__(self) -> int:
            return 8

        def __float__(self) -> float:
            return 1.5

    inst1 = Sample()
    inst2 = DunderSamples()

    m = RQObject(instance=inst1)
    connect_signal(m.rq_data_changed)

    assert m.get() == inst1
    assert isinstance(str(Sample), str)
    with pytest.raises(TypeError):
        int(m)

    with pytest.raises(TypeError):
        float(m)

    m.set(inst2)
    assert_signal_emitted(m.rq_data_changed)
    assert m.get() == inst2
    assert str(m) == "Hello"
    assert int(m) == 8
    assert float(m) == 1.5
