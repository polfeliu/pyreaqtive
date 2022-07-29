from pyreaqtive import rq_getattr

from .qtbot_window import window_fixture


class SampleObject:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


def test_getattr(qtbot, window_fixture):
    inst = SampleObject()

    reactive_count = rq_getattr(inst, "count")
    assert reactive_count.get() == 0

    inst.increment()
    assert reactive_count.get() == 1

    reactive_count.set(10)
    assert inst.count == 10

    same_reactive_count = rq_getattr(inst, "count")
    assert same_reactive_count is reactive_count
