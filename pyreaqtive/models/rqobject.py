from .rqmodel import RQModel


class RQObject(RQModel):
    """Reactive Object Model.

    Represents any object, without a strict type
    """

    def __init__(self, instance: object):
        """Constructor.

        Args:
            instance: Initial object
        """
        super(RQObject, self).__init__()
        self._instance = instance

    def get(self) -> object:
        """Get value of the model.

        Returns:
            object: object of the model
        """
        return self._instance

    def set(self, value: object) -> None:
        """Set value of model.

        Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._instance = value
        self.rq_data_changed.emit()

    def __str__(self) -> str:
        """Get value of the model in string format.

        Returns:
            str: value of the model converted to string
        """
        return self._instance.__str__()

    def __int__(self) -> int:
        """Get value of the model in int format.

        Returns:
            str: value of the model converted to int

        Raises:
            TypeError
        """
        if hasattr(self._instance, "__int__"):
            return self._instance.__int__()  # type: ignore
        else:
            raise TypeError

    def __float__(self) -> float:
        """Get value of the model in float format.

        Returns:
            str: value of the model converted to float

        Raises:
            TypeError
        """
        if hasattr(self._instance, "__float__"):
            return self._instance.__float__()  # type: ignore
        else:
            raise TypeError
