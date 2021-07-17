from .rqmodel import RQModel


class RQFloat(RQModel):
    """
    Reactive Float Model

    Represents a floating point number
    """

    _float: float
    """
    Model store variable
    """

    def __init__(self, initial_float: float):
        """
        Args:
            initial_float: Initial value of the model
        """
        super().__init__()
        self._float = float(initial_float)

    def get(self) -> float:
        """
        Get value of the model

        Returns:
            float: value of the model

        """
        return self._float

    def set(self, value: float) -> None:
        """
        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._float = float(value)
        self._rq_data_changed.emit()

    def __str__(self) -> str:
        """
        Get the value of the model in string format

        Returns:
            str: value of the model converted to string
        """
        return str(self._float)

    def __int__(self) -> int:
        """
        Get the value of the model in integer format

        Returns:
            str: value of the model converted to integer
        """
        return int(self._float)

    def __float__(self) -> float:
        """
        Get the value of the model in float format

        Returns:
            str: value of the model
        """
        return self._float
