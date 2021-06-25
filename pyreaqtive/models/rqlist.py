from .rqmodel import RQModel
from .rqint import RQInt

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from typing import List

class RQList(RQModel):

    _list: list = []

    def __init__(self, initial_models: List[RQModel]=[]):
        for model in initial_models:
            instance = model()
            self._list.append(instance)
        super().__init__()


    _rq_list_insert = pyqtSignal(int)
    _rq_list_remove = pyqtSignal(int)

    def append(self, model):
        instance = model()
        self._list.append(instance)
        self._update_child_indexes()
        self._rq_list_insert.emit(len(self._list) - 1)

    def pop(self):
        if len(self._list) > 0:
            self._list.pop()
            self._update_child_indexes()
            self._rq_list_remove.emit(len(self._list))

    def get_item(self, index):
        return self._list[index]

    def _rq_initialize(self):
        self._update_child_indexes()
        for index, item in enumerate(self._list):
            self._rq_list_insert.emit(index)

    def _update_child_indexes(self):
        for index, item in enumerate(self._list):
            if hasattr(item, "rq_list_index"):
                if isinstance(item.rq_list_index, RQInt):
                    item.rq_list_index.set(index)
