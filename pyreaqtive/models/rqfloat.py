from typing import Callable

from .rqmodel import RQModel, RQComputedModel


class RQFloat(RQModel):
    """Reactive Float Model.

    Represents a floating point number
    """

    def __init__(self, initial_float: float):
        """Constructor.

        Args:
            initial_float: Initial value of the model
        """
        super(RQFloat, self).__init__()
        self._float: float = float(initial_float)
        """Model store variable."""

    def get(self) -> float:
        """Get value of the model.

        Returns:
            float: value of the model
        """
        return self._float

    def set(self, value: float) -> None:
        """Set value of model.

        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._float = float(value)
        self.rq_data_changed.emit()

    def __str__(self) -> str:
        """Get value of the model in string format.

        Returns:
            str: value of the model converted to string
        """
        return str(self.get())

    def __int__(self) -> int:
        """Get value of the model in integer format.

        Returns:
            str: value of the model converted to integer
        """
        return int(self.get())

    def __float__(self) -> float:
        """Get value of the model in float format.

        Returns:
            str: value of the model
        """
        return self.get()


class RQComputedFloat(RQComputedModel, RQFloat):
    """Reactive Computed Float Model."""

    def __init__(self, function: Callable, **kwargs: RQModel):
        """Constructor.

        Args:
            function: function to calculate the model value from input values

            **kwargs: reactive models in the function by variable name as keyword
                Changes in these models will trigger recalculation of the function
       """
        RQFloat.__init__(self, 0)
        RQComputedModel.__init__(self, function, **kwargs)

    def get(self) -> float:
        """Get the computed value."""
        return float(super().get())
