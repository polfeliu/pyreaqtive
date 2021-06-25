from .rqmodel import RQModel
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from typing import List

class RQList(RQModel):

    _list: list = []

    def __init__(self, initial_models: List[RQModel]=[]):
        super().__init__()
        for model in initial_models:
            instance = model()
            self._list.append(instance)

    _rq_list_insert = pyqtSignal(int)
    _rq_list_remove = pyqtSignal(int)

    def append(self, model):
        instance = model()
        self._list.append(instance)
        self._rq_list_insert.emit(len(self._list) - 1)

    def pop(self):
        if len(self._list) > 0:
            self._list.pop()
            self._rq_list_remove.emit(len(self._list))

    def get_item(self, index):
        return self._list[index]

    def _rq_initialize(self):
        for index, item in enumerate(self._list):
            self._rq_list_insert.emit(index)