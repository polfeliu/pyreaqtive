from .rqmodel import RQModel
from .rqint import RQInt

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from typing import List, Type

class RQList(RQModel):

    _list: list

    def __init__(self, initial_models: List[Type[RQModel]]=[]):
        self._list = []
        for model in initial_models:
            instance = model()
            self._list.append(instance)
        self._update_child_indexes()
        super().__init__()


    _rq_list_insert = pyqtSignal(int)
    _rq_list_remove = pyqtSignal(int)

    def append(self, model: Type[RQModel]) -> RQModel:
        instance = model()
        self._list.append(instance)
        self._update_child_indexes()
        self._rq_list_insert.emit(len(self._list) - 1)
        return instance

    def pop(self):
        if len(self._list) > 0:
            self._list.pop()
            self._update_child_indexes()
            self._rq_list_remove.emit(len(self._list))

    def get_item(self, index):
        return self._list[index]

    def get_index(self, item):
        return self._list.index(item)

    def _update_child_indexes(self):
        for index, item in enumerate(self._list):
            if hasattr(item, "rq_list_index"):
                if isinstance(item.rq_list_index, RQInt):
                    item.rq_list_index.set(index)

    def __iter__(self):
        for item in self._list:
            yield item
