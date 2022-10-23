from typing import TYPE_CHECKING

import pytest

from pyreaqtive import rq_getlist

from .qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


class SampleObject:

    def __init__(self) -> None:
        self.numbers = [0]
        self.text = "asdf"

    def add_number(self) -> None:
        self.numbers.append(self.numbers[-1] + 1)


def test_getlist(
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name, unused-argument
) -> None:
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
