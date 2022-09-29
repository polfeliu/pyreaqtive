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

        if self.trigger == self.AutoTriggers.START:
            self.start()
        elif isinstance(trigger, RQModel):
            trigger.rq_data_changed.connect(self.start)
        else:
            raise TypeError

    def run(self) -> None:
        self.working.set(True)
        try:
            self.task()
        except Exception as ex:
            if self.exception_callback is not None:
                self.exception_callback(ex)
        finally:
            self.working.set(False)
