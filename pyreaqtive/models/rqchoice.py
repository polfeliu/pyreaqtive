from typing import Union, Iterator

from .rqlist import RQList
from .rqmodel import RQModel


class RQChoice(RQModel):
    """Reactive Choice Model

    Represents a choice from a list of choices
    """

    def __init__(self, choices: RQList, selected: RQModel = None, allow_none=False):
        """Constructor

        Args:
            choices: Initial list of choices
            selected: Initial choice selected
        """
        super().__init__()
        self.rq_choices_list: RQList = choices
        """Reactive list of available choices"""

        self.selected: Union[RQModel, None] = selected
        """Selected item

        Can be None if allow_none is True
        """

        self.allow_none: bool = allow_none
        """Indicates if model accepts choice none apart from the list of choices"""

        self.validate_selected()
        self.rq_choices_list.rq_list_remove.connect(lambda: self.validate_selected(auto_reset=True))

    def get(self) -> RQModel:
        """Get current selection

        Returns:
            RQModel: Selected Model
        """
        return self.selected

    def get_choices(self) -> RQList:
        """Get list of choices

        Returns:
            RQList: List of choices
        """
        return self.rq_choices_list

    def validate_selected(self, auto_reset=False) -> None:
        """Validate that the current selection is none or is a valid choice from the choices list

        Args:
            auto_reset:
                if True, when selected is not valid resets the selection
                if False, raises KeyError Exception
        """
        if self.selected is None:
            if self.allow_none:
                return
            else:
                raise ValueError

        if self.selected not in self.get_choices():
            if auto_reset:
                self.reset()
            else:
                raise KeyError

    def set(self, value: Union[RQModel, None]) -> None:
        """Set selected option

        Args:
            value: New selected choice
        """
        self.selected = value
        self.validate_selected()
        self.rq_data_changed.emit()

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
        return str(self.selected)

    def __iter__(self) -> Iterator[RQModel]:
        """Iterator of the choices of the list

        Returns:
            Iterator of RQModels
        """
        return self.get_choices().__iter__()
