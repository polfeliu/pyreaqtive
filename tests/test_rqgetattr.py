from typing import TYPE_CHECKING, Union

from pyreaqtive import rq_getattr

from .qtbot_window import window_fixture

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


class SampleObject:

    def __init__(self) -> None:
        self.count = 0

    def increment(self) -> None:
        self.count += 1


def test_getattr(qtbot: 'QtBot', window_fixture: 'QMainWindow') -> None:
    inst = SampleObject()

    reactive_count = rq_getattr(inst, "count")
    assert reactive_count.get() == 0

    inst.increment()
    assert reactive_count.get() == 1

    reactive_count.set(10)
    assert inst.count == 10

    same_reactive_count = rq_getattr(inst, "count")
    assert same_reactive_count is reactive_count
