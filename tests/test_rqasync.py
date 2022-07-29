from pyreaqtive import RQAsync, RQInt
import pytest
from .qtbot_window import window_fixture
from time import sleep

task_triggered = False


def test_rqasync(qtbot, window_fixture):
    def task():
        global task_triggered
        task_triggered = True

    def assert_task_triggered():
        global task_triggered
        assert task_triggered
        task_triggered = False

    inst = RQAsync(
        task,
        trigger=RQAsync.AutoTriggers.Start
    )
    sleep(0.1)
    assert_task_triggered()

    model = RQInt(0)

    inst = RQAsync(
        task,
        trigger=model
    )
    assert not task_triggered

    model.set(5)
    sleep(0.1)
    assert_task_triggered()

    inst.run()
    sleep(0.1)
    assert_task_triggered()

    with pytest.raises(TypeError):
        inst = RQAsync(
            task,
            trigger=None
        )
