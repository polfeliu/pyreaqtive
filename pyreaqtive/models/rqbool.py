from .rqmodel import RQModel, RQComputedModel

from typing import Callable


class RQBool(RQModel):
    """Reactive Boolean Model

    Represents a Boolean
    """

    _bool: bool
    """Model store variable"""

    def __init__(self, state: bool):
        """Constructor

        Args:
            state: Initial state of the model
        """
        super().__init__()
        self._bool = bool(state)

    def get(self) -> bool:
        """Get value of the model

        Returns:
            bool: value of the model

        """
        return self._bool

    def set(self, value: bool) -> None:
        """Set value of model

        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._bool = bool(value)
        self.rq_data_changed.emit()

    def toggle(self) -> None:
        """Toggle the value of the model"""
        self.set(not self.get())

    def __bool__(self) -> bool:
        """Get value of the model in bool format

        Returns:
            bool: value of the model

        """
        return self.get()

    def __str__(self) -> str:
        """Get value of the model in string format

        Returns:
            str: value of the model converted to string
        """
        return str(self.get())


class RQComputedBool(RQComputedModel, RQBool):
    """Reactive Computed Boolean Model"""

    def __init__(self, function: Callable, **kwargs):
        """Constructor

        Args:
            function: function to calculate the model value from input values

            kwargs: reactive models in the function by variable name as keyword
                Changes in these models will trigger recalculation of the function
       """
        RQComputedModel.__init__(self, function, **kwargs)
        RQBool.__init__(self, self.get())

    def get(self) -> bool:
        """Get the computed value"""
        return bool(super(RQComputedBool, self).get())
