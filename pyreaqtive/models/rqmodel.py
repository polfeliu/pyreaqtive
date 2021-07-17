from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot


class RQModel(QObject):
    """
    RQModel Base Class

    All pyreactive models must inherit from this class, that provides basic get, set method and data changed signals
    """

    def get(self):

        """
        Method to get the value of the underlying object

        Must be overridden by model

        Returns:
            Any: value of the object
        """
        raise NotImplementedError

    def set(self, value):
        """
        Method to set the value of the underlying object

        Must be overridden by model

        Args:
            value: New value of the model

        """
        raise NotImplementedError

    _rq_data_changed = pyqtSignal()
    """
    pyqtSignal data changed signal
    
    Widgets that are connected to models can connect slots to this signal.
    The model must emit to this when the state of it changes, to notify the widgets.
    """
