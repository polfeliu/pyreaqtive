from .rqmodel import RQModel, RQComputedModel
from .rqint import RQInt

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from difflib import SequenceMatcher

from typing import List, Iterator, Callable


class RQListIndex(RQInt):
    """Reactive Index of a Item in a List"""

    INVALID_INDEX_VALUE = -1
    """Value if item is not present in list"""

    def __init__(self, item: RQModel, initial: 'RQList'):
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

    def __init__(self, initial_models: List[RQModel] = None):
        """Constructor

        Args:
            initial_models: List of model instances
        """
        self._list: List[RQModel] = initial_models if initial_models is not None else []
        """Model store variable

        Stores instances of models
        """

        RQModel.__init__(self)

    def set(self, value) -> None:
        raise NotImplementedError("Cannot set whole list, insert items one by one")

    def get(self) -> list:
        """Get value of the model

        Returns:
            list: value of the model
        """
        return self._list

    def insert(self, index, model: RQModel) -> None:
        """Insert a model instance to the specified index on the list

        Args:
            index: positional index on the list
            model: Model to be inserted

        Returns:

        """
        model._rq_delete.connect(
            lambda: self.remove_all(model)
        )
        self._list.insert(index, model)
        self.rq_list_insert.emit(index)
        self.rq_data_changed.emit()

    def append(self, model: RQModel) -> None:
        """Append a model instance to the end of the list

        Args:
            model: Model to be appended

        Returns: Instance of the model
        """
        RQList.insert(
            self,
            index=len(self._list),
            model=model
        )

    def __delitem__(self, index) -> None:
        """Delete the item in the list in the specified index

        Args:
            index: positional index on the list
        """
        self.RQList.__delitem__(self, index)
        self.rq_list_remove.emit(index)
        self.rq_data_changed.emit()

    def pop(self) -> None:
        """Delete last instance of the list"""
        RQList.__delitem__(self, len(self._list) - 1)

    def remove(self, item: RQModel) -> None:
        """Remove first occurrence of value

        Args:
            item: model item
        """
        index = RQList.index(self, item)
        self.__delitem__(index)

    def remove_all(self, item: RQModel) -> None:
        """Remove all instances in the list

        Args:
            item: model item
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

    def __getitem__(self, index: int) -> RQModel:
        """Returns the indicated item of the list

        Args:
            index: element of the list

        Returns:
            RQModel: item in the list indicated by index
        """
        return self._list[index]

    def index(self, item: RQModel) -> int:
        """Returns the index where a item is located

        Raises an ValueError if is not in the list

        Args:
            item: instance that should be in the list

        Returns:
            int: index of the item in the list
        """
        return self._list.index(item)

    def reactive_index(self, item: RQModel) -> RQListIndex:
        """Returns a reactive index model that indicates where the item is located

        Args:
            item: instance that should be in the list

        Returns:
            RQListIndex: reactive index of the item in the list
        """
        return RQListIndex(item, self)

    def __iter__(self) -> Iterator[RQModel]:
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

    def extend(self, iterable: List[RQModel]):
        """Same as python list method"""
        for model in iterable:
            self.append(model)

    def __contains__(self, item: RQModel) -> bool:
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

        while True:
            sequence = SequenceMatcher(None, self._list, new_list)
            opcodes = sequence.get_opcodes()

            equal = True

            for operation, i1, i2, j1, j2 in opcodes:

                if operation == 'equal':
                    continue
                else:
                    equal = False

                for x in range(i2 - i1 + 1):
                    if operation == 'insert':
                        super(RQComputedList, self).insert(
                            index=j1 + x,
                            model=new_list[i1 + x]
                        )
                    elif operation == 'delete':
                        super(RQComputedList, self).__delitem__(
                            index=j1 + x
                        )
                    elif operation == 'replace':
                        super(RQComputedList, self).__delitem__(
                            index=j1 + x
                        )
                        super(RQComputedList, self).insert(
                            index=j1 + x,
                            model=new_list[i1 + x]
                        )

            if equal:
                break

    def get(self) -> list:
        """See overridden method

        ComputedLists are recalculated on change, not on request,
        so this just redirects to the actual list.
        """
        return self._list

    def insert(self, index, model: RQModel) -> None:
        raise RuntimeError("Computed Models do not allow insert()")

    def __delitem__(self, key):
        raise RuntimeError("Computed Models do not allow __delitem__()")
