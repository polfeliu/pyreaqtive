from typing import Union
from enum import Enum, auto

from PyQt5.QtCore import QThread

from pyreaqtive import RQBool, RQModel


class RQAsync(QThread):
    class AutoTriggers(Enum):
        Start = auto()  # TODO

    def __init__(self, task, trigger: Union[AutoTriggers, RQModel] = AutoTriggers.Start):
        super(RQAsync, self).__init__()
        self.task = task
        self.trigger = trigger

        self.working = RQBool(False)

        if self.trigger == self.AutoTriggers.Start:
            self.start()
        elif isinstance(trigger, RQModel):
            trigger.rq_data_changed.connect(self.start)

    def run(self) -> None:
        self.working.set(True)
        self.task()
        self.working.set(False)
