import pytest
from tests.signal_checker import connect_signal, assert_signal_emitted

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

    model = RQObject(instance=inst1)
    connect_signal(model.rq_data_changed)

    assert model.get() == inst1
    assert isinstance(str(Sample), str)
    with pytest.raises(TypeError):
        int(model)

    with pytest.raises(TypeError):
        float(model)

    model.set(inst2)
    assert_signal_emitted(model.rq_data_changed)
    assert model.get() == inst2
    assert str(model) == "Hello"
    assert int(model) == 8
    assert float(model) == 1.5
