from PyQt5.QtWidgets import QSpinBox
from ..models import RQModel

class RQSpinBox(QSpinBox):

    model: RQModel = None

    def __init__(self, model, *args):
        self.model = model
        super().__init__(*args)
        self.setValue(self.model)
        self.setRange(-2 ** 30, 2 ** 30)
        self.model._rq_data_changed.connect(
            lambda: self.setValue(int(self.model))
        )

        self.valueChanged.connect(
            lambda: self.model.set(self.value())
        )

