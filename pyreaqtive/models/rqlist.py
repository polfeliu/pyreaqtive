from .rqmodel import RQModel
from .rqint import RQInt

from PyQt5.QtCore import pyqtSignal

from typing import List, Iterator


class RQList(RQModel):
    """Reactive List Model

    Represents a list of model instances

    This model is quite different from the others and doesn't use data_changed signal.
    Instead it uses insert and remove signals that indicate the index of the list where this event is happening.
    This can greatly improve the efficiency of widgets that use this model.
    """

    _list: list
    """Model store variable
    
    Stores instances of models
    """

    def __init__(self, initial_models: List[RQModel] = None):
        """Constructor

        Args:
            initial_models: List of model instances
        """
        self._list = initial_models if initial_models is not None else []
        self._update_child_indexes()
        super().__init__()

    _rq_list_insert = pyqtSignal(int)
    """List insert signal. 
    
    Indicates that there's been an insertion to the position indicated by the int
    """

    _rq_list_remove = pyqtSignal(int)
    """List remove signal. 
    
    Indicates that there's been an deletion in the position indicated by the int
    """

    def set(self, value) -> None:
        raise NotImplementedError("Cannot set whole list, insert items one by one")

    def get(self) -> list:
        """Get value of the model

        Returns:
            list: value of the model
        """
        return self._list

    def insert(self, index, model: RQModel) -> None:
        """Inserts a model instance to the specified index on the list

        Args:
            index: positional index on the list
            model: Model to be inserted

        Returns:

        """
        self._list.insert(index, model)
        self._update_child_indexes()
        self._rq_list_insert.emit(index)

    def append(self, model: RQModel) -> None:
        """Appends a model instance to the end of the list

        Args:
            model: Model to be appended

        Returns: Instance of the model
        """
        self.insert(
            index=len(self._list),
            model=model
        )

    def pop(self) -> None:
        """Delete last instance of the list"""
        if len(self._list) > 0:
            self._list.pop()
            self._update_child_indexes()
            self._rq_list_remove.emit(len(self._list))

    def remove_index(self, index: int) -> None:
        """Remove item in the index of the list

        Args:
            index: index of the list
        """
        if len(self._list) > index:
            del self._list[index]
            self._update_child_indexes()
            self._rq_list_remove.emit(index)

    def remove_item(self, item: RQModel) -> None:
        """Remove item in the list

        Args:
            item: model item
        """
        index = self.get_index(item)
        self.remove_index(index)

    def clear(self) -> None:
        """Clear all items of the list"""
        while len(self) > 0:
            self.pop()

    def get_item(self, index: int) -> RQModel:
        """Returns the indicated item of the list

        Args:
            index: element of the list

        Returns:
            RQModel: item in the list indicated by index
        """
        return self._list[index]

    def get_index(self, item: RQModel) -> int:
        """Returns the index where a item is located

        Raises an ValueError if is not in the list

        Args:
            item: instance that should be in the list

        Returns:
            int: index of the item in the list
        """
        return self._list.index(item)

    def _update_child_indexes(self) -> None:
        """Injects the index of the list to all children,
        if they have an attribute rq_list_index that is a RQInt
        """
        for index, item in enumerate(self._list):
            if hasattr(item, "rq_list_index"):
                if isinstance(item.rq_list_index, RQInt):
                    item.rq_list_index.set(index)

    def __iter__(self) -> Iterator[RQModel]:
        """Iterator of the elements of the list

        Returns:
            Iterator of RQModels
        """
        for item in self._list:
            yield item

    def __len__(self):
        """Length of the list"""
        return len(self._list)

    def count(self, value):
        """Same as python list method"""
        self._list.count(value)

    def extend(self, iterable: List[RQModel]):
        """Same as python list method"""
        for model in iterable:
            self.append(model)
