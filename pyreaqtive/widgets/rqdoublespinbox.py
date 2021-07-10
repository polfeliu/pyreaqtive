from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQFloat


class RQDoubleSpinBox(QDoubleSpinBox):
    model: RQFloat

    def __init__(self, model, *args):
        super().__init__(*args)
        self.model = model
        self._rq_data_changed()
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.valueChanged.connect(self._valueChanged)

    @pyqtSlot()
    def _rq_data_changed(self):
        if not self._rq_self_changing:
            self.setValue(float(self.model))

    _rq_self_changing = False

    @pyqtSlot()
    def _valueChanged(self):
        self._rq_self_changing = True
        self.model.set(self.value())
        self._rq_self_changing = False
