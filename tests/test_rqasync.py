from typing import TYPE_CHECKING
from time import sleep

import pytest
import pytest_cases

from pyreaqtive import RQAsync, RQInt

from .qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow

TASK_TRIGGERED = False
EXCEPTION_TRIGGERED = False
TRIGGER_EXCEPTION = False
SLOW_TASK = False


@pytest_cases.parametrize("exception_callback", [True, False])
def test_rqasync(
        exception_callback: bool,
        qtbot: 'QtBot',  # pylint: disable=unused-argument, unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    global TASK_TRIGGERED
    global EXCEPTION_TRIGGERED
    global TRIGGER_EXCEPTION
    global SLOW_TASK

    TASK_TRIGGERED = False  # pylint: disable=redefined-outer-name
    EXCEPTION_TRIGGERED = False  # pylint: disable=redefined-outer-name
    TRIGGER_EXCEPTION = False  # pylint: disable=redefined-outer-name
    SLOW_TASK = False  # pylint: disable=redefined-outer-name

    def task() -> None:
        global TASK_TRIGGERED
        TASK_TRIGGERED = True

        print("Running")
        if TRIGGER_EXCEPTION:
            print("Triggering exception")
            raise ValueError

        if SLOW_TASK:
            print("slowing task")
            sleep(1)

        print("Finished")

    def exception(_: Exception) -> None:
        global EXCEPTION_TRIGGERED
        EXCEPTION_TRIGGERED = True
        print("Capturing exception")

    def assert_task_triggered() -> None:
        global TASK_TRIGGERED
        assert TASK_TRIGGERED
        TASK_TRIGGERED = False

    def assert_exception(status: bool) -> None:
        global EXCEPTION_TRIGGERED
        assert EXCEPTION_TRIGGERED == status
        EXCEPTION_TRIGGERED = False

    inst = RQAsync(
        task,
        trigger=RQAsync.AutoTriggers.START,
    )
    sleep(0.1)
    assert_task_triggered()

    model = RQInt(0)

    inst = RQAsync(
        task,
        trigger=model,
        exception_callback=exception if exception_callback else None
    )
    assert not TASK_TRIGGERED

    TRIGGER_EXCEPTION = False
    model.set(5)
    sleep(0.1)
    assert_task_triggered()
    assert_exception(False)

    inst.run()
    sleep(0.1)
    assert_task_triggered()
    assert_exception(False)

    TRIGGER_EXCEPTION = True
    inst.run()
    sleep(0.1)
    assert_task_triggered()
    assert_exception(exception_callback)

    with pytest.raises(TypeError):
        inst = RQAsync(
            task,
            trigger=None  # type: ignore
        )

    TRIGGER_EXCEPTION = False
    SLOW_TASK = True
    inst.start()
    sleep(0.1)
    assert inst.working
    assert inst._served_trigger  # pylint: disable=protected-access

    assert_task_triggered()

    inst.start()
    sleep(0.1)
    assert inst.working
    assert not inst._served_trigger  # pylint: disable=protected-access

    # Ensure the slow task has finished
    sleep(1.5)  # type: ignore
