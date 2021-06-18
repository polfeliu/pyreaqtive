from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQModel

class RQCheckbox(QCheckBox):

    model: RQModel = None

    def __init__(self, model, *args):
        super().__init__(*args)
        self.model = model
        self.toggled.connect(self._toggled)
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self):
        self.setChecked(bool(self.model))

    @pyqtSlot()
    def _toggled(self):
        self.model.set(bool(self.checkState()))