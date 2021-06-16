from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

class RQModel(QObject):
    pass

class RQInt(RQModel):

    _int: int

    def __init__(self, integer):
        super().__init__()
        self._int = integer

    def get(self):
        return self._int

    def set(self, value):
        self._rq_data_changed.emit()
        self._int = value

    def __str__(self):
        return str(self._int)

    _rq_data_changed = pyqtSignal()

