from PyQt5.QtCore import QThread

from pyreaqtive import RQBool


class RQAsync(QThread):
    Start = object()

    def __init__(self, task, trigger=Start):
        super(RQAsync, self).__init__()
        self.task = task
        self.trigger = trigger

        self.working = RQBool(False)

        if self.trigger == self.Start:
            self.start()

    def run(self) -> None:
        self.working.set(True)
        self.task()
        self.working.set(False)
