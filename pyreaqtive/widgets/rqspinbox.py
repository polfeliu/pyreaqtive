from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQModel

class RQSpinBox(QSpinBox):

    model: RQModel = None

    def __init__(self, model, *args):
        self.model = model
        super().__init__(*args)
        self.setValue(self.model)
        self.setRange(-2 ** 30, 2 ** 30)
        self.model._rq_data_changed.connect(self._rq_data_changed)

        self.valueChanged.connect(self._valueChanged)

    @pyqtSlot()
    def _rq_data_changed(self):
        self.setValue(int(self.model))

    @pyqtSlot()
    def _valueChanged(self):
        self.model.set(self.value())

