from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQModel

class RQLabel(QLabel):

    model: RQModel = None

    def __init__(self, model, *args):
        super().__init__(str(self.model), *args)
        self.model = model
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    def _rq_data_changed(self):
        self.setText(str(self.model))
