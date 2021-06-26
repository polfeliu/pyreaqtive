from PyQt5.QtWidgets import QProgressBar

from ..models import RQInt

class RQProgressBar(QProgressBar):

    model: RQInt

    def __init__(self, model: RQInt, *args):
        self.model = model
        super().__init__(*args)

        self.model._rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    def _rq_data_changed(self):
        self.setValue(self.model.get())