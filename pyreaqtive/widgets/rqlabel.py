from PyQt5.QtWidgets import QLabel
from ..models import RQModel

class RQLabel(QLabel):

    model: RQModel = None

    def __init__(self, model, *args):
        self.model = model
        self.model._rq_data_changed.connect(
            lambda: self.setText(str(self.model))
        )

        super().__init__(str(self.model), *args)
