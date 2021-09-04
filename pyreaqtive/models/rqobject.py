from .rqmodel import RQModel, RQComputedModel

from typing import Callable, Any


class RQObject(RQModel):

    def __init__(self, instance: object):
        super().__init__()
        self._instance = instance

    def get(self) -> object:
        return self._instance

    def set(self, instance: object) -> None:
        self._instance = instance
        self.rq_data_changed.emit()

