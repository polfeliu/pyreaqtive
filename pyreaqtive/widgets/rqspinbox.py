from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQModel

class RQSpinBox(QSpinBox):

    model: RQModel = None

    def __init__(self, model, *args):
        super().__init__(*args)
        self.model = model
        self.setValue(self.model)
        self.setRange(-2 ** 30, 2 ** 30)
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.valueChanged.connect(self._valueChanged)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self):
        if not self._rq_self_changing:
            self.setValue(int(self.model))

    _rq_self_changing = False

    @pyqtSlot()
    def _valueChanged(self):
        self._rq_self_changing = True
        self.model.set(self.value())
        self._rq_self_changing = False

