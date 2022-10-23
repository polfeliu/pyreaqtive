from typing import TYPE_CHECKING

from pyreaqtive import RQAsync, RQInt
import pytest
import pytest_cases
from .qtbot_window import window_fixture
from time import sleep

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow

task_triggered = False
exception_triggered = False
trigger_exception = False
slow_task = False


@pytest_cases.parametrize("exception_callback", [True, False])
def test_rqasync(exception_callback: bool, qtbot: 'QtBot', window_fixture: 'QMainWindow') -> None:
    global trigger_exception
    global exception_triggered
    global trigger_exception
    global slow_task

    task_triggered = False
    exception_triggered = False
    trigger_exception = False
    slow_task = False

    def task() -> None:
        global task_triggered
        task_triggered = True

        global trigger_exception
        print("Running")
        if trigger_exception:
            print("Triggering exception")
            raise ValueError

        if slow_task:
            print("slowing task")
            sleep(1)

        print("Finished")

    def exception(ex: Exception) -> None:
        global exception_triggered
        exception_triggered = True
        print("Capturing exception")

    def assert_task_triggered() -> None:
        global task_triggered
        assert task_triggered
        task_triggered = False

    def assert_exception(status: bool) -> None:
        global exception_triggered
        assert exception_triggered == status
        exception_triggered = False

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
    assert not task_triggered

    trigger_exception = False
    model.set(5)
    sleep(0.1)
    assert_task_triggered()
    assert_exception(False)

    inst.run()
    sleep(0.1)
    assert_task_triggered()
    assert_exception(False)

    trigger_exception = True
    inst.run()
    sleep(0.1)
    assert_task_triggered()
    assert_exception(exception_callback)

    with pytest.raises(TypeError):
        inst = RQAsync(
            task,
            trigger=None  # type: ignore
        )

    trigger_exception = False
    slow_task = True
    inst.start()
    sleep(0.1)
    assert inst.working
    assert inst._served_trigger
    assert_task_triggered()

    inst.start()
    sleep(0.1)
    assert inst.working
    assert not inst._served_trigger

    # Ensure the slow task has finished
    sleep(1.5)  # type: ignore
