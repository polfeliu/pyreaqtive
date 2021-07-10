from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQModel


class RQLineEdit(QLineEdit):
    model: RQModel

    def __init__(self, model, *args):
        self.model = model
        super().__init__(*args)
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.textChanged.connect(self._valueChanged)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self):
        if not self._rq_self_changing:
            self.setText(str(self.model))

    _rq_self_changing = False

    @pyqtSlot(str)
    def _valueChanged(self, text):
        self._rq_self_changing = True
        self.model.set(text)
        self._rq_self_changing = False
