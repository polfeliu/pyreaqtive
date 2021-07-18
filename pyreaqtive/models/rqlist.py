from .rqmodel import RQModel
from .rqint import RQInt

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from typing import List, Type, Iterator


class RQList(RQModel):
    """
    Reactive List Model

    Represents a list of model instances

    Both the constructor and append functions take the class and
    create the instance internally.

    This model is quite different from the others and doesn't use data_changed signal.
    Instead it uses insert and remove signals that indicate the index of the list where this event is happening.
    This can greatly improve the efficiency of widgets that use this model.
    """

    _list: list
    """
    Model store variable
    
    Stores instances of models
    """

    def __init__(self, initial_models: List[Type[RQModel]] = []):
        """
        Args:
            initial_models: List of models to be instantiated
        """
        self._list = []
        for model in initial_models:
            instance = model()
            self._list.append(instance)
        self._update_child_indexes()
        super().__init__()

    _rq_list_insert = pyqtSignal(int)
    """
    List insert signal. Indicates that there's been an insertion to the position indicated by the int
    """

    _rq_list_remove = pyqtSignal(int)
    """
    List remove signal. Indicates that there's been an deletion in the position indicated by the int
    """

    def append(self, model: Type[RQModel]) -> RQModel:
        """
        Appends a model instance to the end of the list

        Args:
            model: Model to be instantiated

        Returns: Instance of the model
        """
        instance = model()
        self._list.append(instance)
        self._update_child_indexes()
        self._rq_list_insert.emit(len(self._list) - 1)
        return instance

    def pop(self) -> None:
        """
        Delete last instance of the list
        """
        if len(self._list) > 0:
            self._list.pop()
            self._update_child_indexes()
            self._rq_list_remove.emit(len(self._list))

    def get_item(self, index) -> RQModel:
        """
        Returns the indicated item of the list

        Args:
            index: element of the list

        Returns:
            RQModel: item in the list indicated by index

        """
        return self._list[index]

    def get_index(self, item) -> int:
        """
        Returns the index where a item is located

        Raises an ValueError if is not in the list

        Args:
            item: instance that should be in the list

        Returns:
            int: index of the item in the list

        """
        return self._list.index(item)

    def _update_child_indexes(self) -> None:
        """
        Injects the index of the list to all childs,
        if they have an attribute rq_list_index that is a RQInt
        """
        for index, item in enumerate(self._list):
            if hasattr(item, "rq_list_index"):
                if isinstance(item.rq_list_index, RQInt):
                    item.rq_list_index.set(index)

    def __iter__(self) -> Iterator[RQModel]:
        """
        Iterator of the elements of the list

        Returns:
            Iterator of RQModels
        """
        for item in self._list:
            yield item
