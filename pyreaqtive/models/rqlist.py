from difflib import SequenceMatcher
from typing import List, Iterator, Callable, Any

from PyQt5.QtCore import pyqtSignal

from .rqint import RQInt
from .rqmodel import RQModel, RQComputedModel

from .sequence_matching import sequence_matching


class RQListIndex(RQInt):
    """Reactive Index of a Item in a List"""

    INVALID_INDEX_VALUE = -1
    """Value if item is not present in list"""

    def __init__(self, item: Any, initial: 'RQList'):
        """Constructor

        Args:
            item: item that presumably is on the list
            initial: list where to search the item
        """
        self.item = item
        self.list = initial
        super(RQListIndex, self).__init__(self._get_index_int())
        self.list.rq_data_changed.connect(
            lambda: self.set(self._get_index_int())
        )

    def _get_index_int(self) -> int:
        try:
            index = self.list.index(self.item)
        except ValueError:
            index = self.INVALID_INDEX_VALUE

        return index


class RQList(RQModel):
    """Reactive List Model

    Represents a list of model instances

    This model is quite different from the others and doesn't use data_changed signal.
    Instead it uses insert and remove signals that indicate the index of the list where this event is happening.
    This can greatly improve the efficiency of widgets that use this model.
    """

    rq_list_insert = pyqtSignal(int)
    """List insert signal. 

    Indicates that there's been an insertion to the position indicated by the int
    """

    rq_list_remove = pyqtSignal(int)
    """List remove signal. 

    Indicates that there's been an deletion in the position indicated by the int
    """

    def __init__(self, initial_items: List[Any] = None):
        """Constructor

        Args:
            initial_items: List of items
        """
        self._list: List[Any] = initial_items if initial_items is not None else []
        """Model store variable

        Stores list of instances
        """

        RQModel.__init__(self)

    def set(self, items: List[Any]) -> None:
        self.clear()
        for item in items:
            self.append(item)

    def get(self) -> list:
        """Get value of the model

        Returns:
            list: value of the model
        """
        return self._list

    def insert(self, index: int, item: Any) -> None:
        """Insert a item to the specified index on the list

        Args:
            index: positional index on the list
            item: item to be inserted

        Returns:

        """
        if isinstance(item, RQModel):
            item._rq_delete.connect(
                lambda: self.remove_all(item)
            )
        self._list.insert(index, item)
        self.rq_list_insert.emit(index)
        self.rq_data_changed.emit()

    def append(self, item: Any) -> None:
        """Append a item to the end of the list

        Args:
            item: Item to be appended
        """
        RQList.insert(
            self,
            index=len(self._list),
            item=item
        )

    def __delitem__(self, key) -> None:
        """Delete the item in the list in the specified index

        Args:
            key: positional index on the list
        """
        self._list.__delitem__(key)
        self.rq_list_remove.emit(key)
        self.rq_data_changed.emit()

    def pop(self) -> None:
        """Delete last instance of the list"""
        RQList.__delitem__(self, len(self._list) - 1)

    def remove(self, item: Any) -> None:
        """Remove first occurrence of value

        Args:
            item: item
        """
        index = RQList.index(self, item)
        self.__delitem__(index)

    def remove_all(self, item: Any) -> None:
        """Remove all instances in the list

        Args:
            item: item
        """
        while True:
            try:
                self.remove(item)
            except ValueError:
                break

    def clear(self) -> None:
        """Clear all items of the list"""
        while len(self) > 0:
            self.pop()

    def __getitem__(self, index: int) -> Any:
        """Returns the indicated item of the list

        Args:
            index: element of the list

        Returns:
            Any: item in the list indicated by index
        """
        return self._list[index]

    def index(self, item: Any) -> int:
        """Returns the index where a item is located

        Raises an ValueError if is not in the list

        Args:
            item: instance that should be in the list

        Returns:
            int: index of the item in the list
        """
        return self._list.index(item)

    def reactive_index(self, item: Any) -> RQListIndex:
        """Returns a reactive index model that indicates where the item is located

        Args:
            item: instance that should be in the list

        Returns:
            RQListIndex: reactive index of the item in the list
        """
        return RQListIndex(item, self)

    def __iter__(self) -> Iterator[Any]:
        """Iterator of the elements of the list

        Returns:
            Iterator of RQModels
        """
        for item in self._list:
            yield item

    def __len__(self) -> int:
        """Length of the list"""
        return len(self._list)

    def count(self, value) -> int:
        """Same as python list method"""
        return self._list.count(value)

    def extend(self, iterable: List[Any]):
        """Same as python list method"""
        for item in iterable:
            self.append(item)

    def __contains__(self, item: Any) -> bool:
        """Same as python list method"""
        return self._list.__contains__(item)


class RQComputedList(RQList, RQComputedModel):
    """Reactive Computed List Model"""

    def __init__(self, function: Callable, **kwargs):
        """Constructor

        Args:
            function: function to calculate the model value from input values

            **kwargs: reactive models in the function by variable name as keyword
                Changes in these models will trigger recalculation of the function
        """
        RQList.__init__(self, [])
        RQComputedModel.__init__(self, function, **kwargs)

    def _variable_changed(self) -> None:
        """Variable changed slot

        Called when some of the models have emitted rq_data_changed.

        Recalculates the list with the function and calculates differences with the current list,
        inserting and deleting the differences.
        """
        # Recompute list
        new_list = RQComputedModel.get(self)

        # Apply operations to current list so it's the same as the newly computed
        sequence_matching(
            modifiable_list=self,
            target_list=new_list
        )

    def get(self) -> list:
        """See overridden method

        ComputedLists are recalculated on change, not on request,
        so this just redirects to the actual list.
        """
        return self._list
