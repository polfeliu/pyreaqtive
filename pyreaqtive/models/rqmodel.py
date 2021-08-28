from PyQt5.QtCore import QObject, pyqtSignal

from typing import Any


class RQModel(QObject):
    """RQModel Base Class

    All pyreaqtive models must inherit from this class, that provides basic get, set method and data changed signals
    """

    def get(self) -> Any:
        """Method to get the value of the underlying object

        Must be overridden by model

        Returns:
            Any: value of the object
        """
        raise NotImplementedError

    def set(self, value: Any) -> None:
        """Method to set the value of the underlying object

        Must be overridden by model

        Args:
            value: New value of the model
        """
        raise NotImplementedError

    rq_data_changed = pyqtSignal()
    """pyqtSignal data changed signal
    
    Widgets that are connected to models can connect slots to this signal.
    The model must emit to this when the state of it changes, to notify the widgets.
    """

    _rq_delete = pyqtSignal()
    """pyqtSignal delete signal
    
    Signals that the model instance is about to be deleted
    """

    def __delete__(self):
        self._rq_delete.emit()
