from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

class RQModel(QObject):

    def get(self):
        raise NotImplementedError

    def set(self, value):
        raise NotImplementedError

    _rq_data_changed = pyqtSignal()