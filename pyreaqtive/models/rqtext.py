from .rqmodel import RQModel


class RQText(RQModel):
    """
    Reactive Text Model

    Represents a string of text
    """

    _text: str
    """
    Model store variable
    """

    def __init__(self, text: str):
        """
        Args:
            text: Initial value of the model
        """
        super().__init__()
        self._text = text

    def get(self) -> str:
        """
        Get value of the model

        Returns:
            str: value of the model
        """
        return self._text

    def set(self, value: str) -> None:
        """
        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._text = value
        self._rq_data_changed.emit()

    def __str__(self) -> str:
        """
        Get value of the model in string format

        Returns:
            str: value of the model
        """
        return self._text
