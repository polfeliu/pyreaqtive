from .rqmodel import RQModel


class RQInt(RQModel):
    """
    Reactive Integer Model
    
    Represents a initial_integer number
    """

    _int: int
    """
    Model store variable
    """

    def __init__(self, initial_integer: int):
        """
        Args:
            initial_integer: Initial value of the model
        """
        super().__init__()
        self._int = int(initial_integer)

    def get(self) -> int:
        """
        Get value of the model

        Returns:
            int: value of the model
        """
        return self._int

    def set(self, value: int) -> None:
        """
        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._int = int(value)
        self._rq_data_changed.emit()

    def increment(self, delta=1) -> None:
        """
        Increment integer method

        Args:
            delta: Increment value. Default 1
        """
        self.set(self._int + delta)

    def decrement(self, delta=1):
        """
        Decrement integer method

        Args:
            delta: Decrement value. Default 1
        """
        self.increment(delta=-delta)

    def __str__(self):
        """
        Get value of the model in string format

        Returns:
            str: value of the model converted to string
        """
        return str(self._int)

    def __int__(self):
        """
        Get value of the model in integer format

        Returns:
            str: value of the model
        """
        return self._int

    def __float__(self):
        """
        Get value of the model in float format

        Returns:
            str: value of the model converted to float
        """
        return float(self._int)
