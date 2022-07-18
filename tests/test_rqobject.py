import pytest

from pyreaqtive import RQObject


def test_object():
    class Sample:
        pass

    class DunderSamples:
        def __str__(self):
            return "Hello"

        def __int__(self):
            return 8

        def __float__(self):
            return 1.5

    inst1 = Sample()
    inst2 = DunderSamples()

    m = RQObject(instance=inst1)
    assert m.get() == inst1
    assert isinstance(str(Sample), str)
    with pytest.raises(TypeError):
        int(m)

    with pytest.raises(TypeError):
        float(m)

    m.set(inst2)
    assert m.get() == inst2
    assert str(m) == "Hello"
    assert int(m) == 8
    assert float(m) == 1.5
