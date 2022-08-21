from enum import Enum, auto
from typing import TYPE_CHECKING, Union, Callable, Any

from qtpy.QtCore import QThread  # type: ignore

from pyreaqtive import RQBool, RQModel

if TYPE_CHECKING:
    from PyQt5.QtCore import QThread


class RQAsync(QThread):
    class AutoTriggers(Enum):
        START = auto()

    def __init__(self, task: Callable[[], Any], trigger: Union[AutoTriggers, RQModel] = AutoTriggers.START):
        super(RQAsync, self).__init__()
        self.task = task
        self.trigger = trigger

        self.working = RQBool(False)

        if self.trigger == self.AutoTriggers.START:
            self.start()
        elif isinstance(trigger, RQModel):
            trigger.rq_data_changed.connect(self.start)
        else:
            raise TypeError

    def run(self) -> None:
        self.working.set(True)
        self.task()
        self.working.set(False)
