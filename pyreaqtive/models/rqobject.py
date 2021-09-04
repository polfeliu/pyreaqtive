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

    def __str__(self):
        return self._instance.__str__()

    def __int__(self):
        if hasattr(self._instance, "__int__"):
            return self._instance.__int__()
        else:
            raise TypeError
