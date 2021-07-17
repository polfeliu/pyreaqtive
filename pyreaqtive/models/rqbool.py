from .rqmodel import RQModel


class RQBool(RQModel):
    """
    Reactive Boolean Model
    """

    _bool: bool
    """
    Model Store Variable
    """

    def __init__(self, state):
        """
        Args:
            state: Initial state of the model
        """
        super().__init__()
        self._bool = state

    def get(self) -> bool:
        """
        Get value of the model

        Returns:
            bool: value of the model

        """
        return self._bool

    def set(self, value) -> None:
        """
        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._bool = value
        self._rq_data_changed.emit()

    def toggle(self):
        """
        Toggle the value of the model
        """
        self.set(not self.get())

    def __bool__(self):
        """
        Get the value of the model in bool format

        Returns:
            bool: value of the model

        """
        return self._bool
