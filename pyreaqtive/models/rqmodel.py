from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot


class RQModel(QObject):
    """
    RQModel Base Class
    All pyqtreactive models must inherit from this class, that provides basic get, set method and data changed signals
    """

    def get(self):
        """
        Method to get the value of the underlying object
        Must be overridden by model
        :return: value of the object
        """
        raise NotImplementedError

    def set(self, value):
        """
        Method to set the value of the underlying object
        Must be overridden by model
        :param value: value to be set to the object
        :return: None
        """
        raise NotImplementedError

    _rq_data_changed = pyqtSignal()
