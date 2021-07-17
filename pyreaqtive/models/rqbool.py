from .rqmodel import RQModel


class RQBool(RQModel):
    """
    Reactive Boolean Model

    Represents a Boolean
    """

    _bool: bool
    """
    Model store variable
    """

    def __init__(self, state: bool):
        """
        Args:
            state: Initial state of the model
        """
        super().__init__()
        self._bool = bool(state)

    def get(self) -> bool:
        """
        Get value of the model

        Returns:
            bool: value of the model

        """
        return self._bool

    def set(self, value: bool) -> None:
        """
        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._bool = bool(value)
        self._rq_data_changed.emit()

    def toggle(self) -> None:
        """
        Toggle the value of the model
        """
        self.set(not self.get())

    def __bool__(self) -> bool:
        """
        Get the value of the model in bool format

        Returns:
            bool: value of the model

        """
        return self._bool

    def __str__(self) -> str:
        """
        Get the value of the model in string format

        Returns:
            str: value of the model converted to string
        """
        return str(self._bool)
