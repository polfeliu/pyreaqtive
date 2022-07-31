from pyreaqtive import rq_getlist
import pytest
from .qtbot_window import window_fixture


class SampleObject:

    def __init__(self):
        self.numbers = [0]
        self.text = "asdf"

    def add_number(self):
        self.numbers.append(self.numbers[-1] + 1)


def test_getlist(qtbot, window_fixture):
    inst = SampleObject()

    reactive_list = rq_getlist(inst, "numbers")
    assert reactive_list.get() == [0]

    inst.add_number()
    assert reactive_list.get() == [0, 1]

    inst.add_number()
    assert reactive_list.get() == [0, 1, 2]

    same_reactive_list = rq_getlist(inst, "numbers")
    assert same_reactive_list is reactive_list

    with pytest.raises(TypeError):
        rq_getlist(inst, "text")
