from .rqmodel import RQModel
from .rqlist import RQList

from typing import Union
from PyQt5.QtCore import pyqtSlot


class RQChoice(RQModel):
    """Reactive Choice Model

    Represents a choice from a list of choices
    """

    _choices: RQList
    """Reactive list of available choices"""

    _selected: Union[RQModel, None]
    """Reactive selected item
    
    Can be None if allow_none is True
    """

    allow_none: bool
    """Indicates if model accepts choice none appart from the list of choices"""

    def __init__(self, choices: RQList, selected: RQModel = None, allow_none=False):
        """Constructor

        Args:
            choices: Initial list of choices

            selected: Initial choice selected
        """
        super().__init__()
        self._choices = choices
        self._selected = selected
        self.allow_none = allow_none
        self.validate_selected()
        self._choices._rq_list_remove.connect(lambda: self.validate_selected(auto_reset=True))

    def get(self) -> RQModel:
        """Get current selection

        Returns:
            RQModel: Selected Model
        """
        return self._selected

    def get_choices(self) -> RQList:
        """Get list of choices

        Returns:
            RQList: List of choices
        """
        return self._choices

    def validate_selected(self, auto_reset=False) -> None:
        """Validate that the current selection is none or is a valid choice from the choices list

        Args:
            auto_reset:
                if True, when selected is not valid resets the selection
                if False, raises KeyError Exception
        """
        if self._selected is None:
            if self.allow_none:
                return
            else:
                raise ValueError

        if self._selected not in self._choices:
            if auto_reset:
                self.reset()
            else:
                raise KeyError

    def set(self, value: Union[RQModel, None]) -> None:
        """Set selected option

        Args:
            value: New selected choice

        Returns:

        """
        self._selected = value
        self.validate_selected()
        self._rq_data_changed.emit()

    def reset(self) -> None:
        """Reset selection to default value

        If allow_none is True default is None, else is the first element
        """
        if self.allow_none:
            self.set(None)
        else:
            self.set(self[0])

    def __str__(self) -> str:
        """Get current choice in string format

        Returns:
            str: value in string of the current choice model

        """
        return str(self._selected)
