from typing import Callable

from .rqmodel import RQModel, RQComputedModel


class RQInt(RQModel):
    """Reactive Integer Model.
    
    Represents a initial_integer number
    """

    def __init__(self, initial_integer: int):
        """Constructor.

        Args:
            initial_integer: Initial value of the model
        """
        super(RQInt, self).__init__()
        self._int: int = int(initial_integer)
        """Model store variable"""

    def get(self) -> int:
        """Get value of the model.

        Returns:
            int: value of the model
        """
        return self._int

    def set(self, value: int) -> None:
        """Set value of model.

        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._int = int(value)
        self.rq_data_changed.emit()

    def increment(self, delta: int = 1) -> None:
        """Increment integer method.

        Args:
            delta: Increment value. Default 1
        """
        self.set(self._int + delta)

    def decrement(self, delta: int = 1) -> None:
        """Decrement integer method.

        Args:
            delta: Decrement value. Default 1
        """
        self.increment(delta=-delta)

    def __str__(self) -> str:
        """Get value of the model in string format.

        Returns:
            str: value of the model converted to string
        """
        return str(self._int)

    def __int__(self) -> int:
        """Get value of the model in integer format.

        Returns:
            str: value of the model
        """
        return self.get()

    def __float__(self) -> float:
        """Get value of the model in float format.

        Returns:
            str: value of the model converted to float
        """
        return float(self.get())


class RQComputedInt(RQComputedModel, RQInt):
    """Reactive Computed Integer Model."""

    def __init__(self, function: Callable, **kwargs: RQModel):
        """Constructor.

        Args:
            function: function to calculate the model value from input values

            **kwargs: reactive models in the function by variable name as keyword
                Changes in these models will trigger recalculation of the function
       """
        RQInt.__init__(self, 0)
        RQComputedModel.__init__(self, function, **kwargs)

    def get(self) -> int:
        """Get the computed value."""
        return int(super().get())
