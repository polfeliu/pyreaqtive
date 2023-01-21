from typing import TYPE_CHECKING

from pyreaqtive import rq_getattr

from .qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


class SampleObject:

    def __init__(self) -> None:
        self.count = 0

    def increment(self) -> None:
        self.count += 1


def test_getattr(
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    inst = SampleObject()

    reactive_count = rq_getattr(inst, "count")
    assert reactive_count.get() == 0

    inst.increment()
    assert reactive_count.get() == 1

    reactive_count.set(10)
    assert inst.count == 10

    same_reactive_count = rq_getattr(inst, "count")
    assert same_reactive_count is reactive_count
