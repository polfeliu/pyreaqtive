from PyQt5.QtWidgets import QCheckBox
from ..models import RQModel

class RQCheckbox(QCheckBox):

    model: RQModel = None

    def __init__(self, model, *args):
        self.model = model
        super().__init__(*args)
        self.setChecked(bool(self.model))
        self.toggled.connect(
            lambda: self.model.set(bool(self.checkState()))
        )
        self.model._rq_data_changed.connect(
            lambda : self.setChecked(bool(self.model))
        )