from enum import Enum, auto
from typing import TYPE_CHECKING, Union, Callable, Any, Optional

from qtpy.QtCore import QThread  # type: ignore

from pyreaqtive import RQBool, RQModel

if TYPE_CHECKING:
    from PyQt5.QtCore import QThread


class RQAsync(QThread):
    class AutoTriggers(Enum):
        START = auto()

    def __init__(self,
                 task: Callable[[], Any],
                 trigger: Union[AutoTriggers, RQModel] = AutoTriggers.START,
                 exception_callback: Optional[Callable[[Exception], Any]] = None
                 ):
        super(RQAsync, self).__init__()
        self.task = task
        self.trigger = trigger
        self.exception_callback = exception_callback

        self.working = RQBool(False)
        self._served_trigger = False

        if self.trigger == self.AutoTriggers.START:
            self.start()
        elif isinstance(trigger, RQModel):
            trigger.rq_data_changed.connect(self.start)
        else:
            raise TypeError

    def start(self, priority: int = QThread.InheritPriority) -> None:
        self._served_trigger = False
        if not self.working:
            super().start(priority)

    def run(self) -> None:
        self.working.set(True)
        self._served_trigger = False
        while not self._served_trigger:
            self._served_trigger = True
            try:
                self.task()
            except Exception as ex:
                if self.exception_callback is not None:
                    self.exception_callback(ex)

        self.working.set(False)
