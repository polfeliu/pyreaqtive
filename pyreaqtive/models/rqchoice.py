from .rqmodel import RQModel
from .rqlist import RQList

from typing import List, Union


class RQChoice(RQModel):
    """
    Reactive Choice Model

    Represents a choice from a list of choices
    """

    _choices: RQList
    """
    Reactive list of available choices
    """

    _selected: Union[RQModel, None]
    """
    Reactive selected item
    """

    def __init__(self, choices: RQList, selected: RQModel = None):
        """
        Args:
            choices: Initial list of choices

            selected: Initial choice selected
        """
        super().__init__()
        self._choices = choices
        self._selected = selected
        self.validate_selected()

    def get(self) -> RQModel:
        """
        Get current selection

        Returns:
            RQModel: Selected Model
        """
        return self._selected

    def get_choices(self) -> RQList:
        """
        Get list of choices

        Returns:
            RQList: List of choices
        """
        return self._choices

    def validate_selected(self) -> None:
        """
        Validate that the current selection is none or is a valid choice from the choices list

        Raises an exception if the current selection is not valid
        """
        if self._selected is None:
            return
        if self._selected not in self._choices:
            raise KeyError

    def set(self, value: RQModel) -> None:
        """
        Set selected option

        Args:
            value: New selected choice

        Returns:

        """
        self._selected = value
        self.validate_selected()
        self._rq_data_changed.emit()

    def __str__(self) -> str:
        """
        Get current choice in string format

        Returns:
            str: value in string of the current choice model

        """
        return str(self._selected)
