from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQFloat


class RQDoubleSpinBox(QDoubleSpinBox):
    """
    Reactive DoubleSpinBox Widget
    """

    model: RQFloat
    """
    Model linked to the widget
    """

    def __init__(self, model, *args):
        """
        Args:
            model: Model to link the widget to

            args: arguments to pass to the native pyqt doublespinbox widget
        """
        super().__init__(*args)
        self.model = model
        self._rq_data_changed()
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.valueChanged.connect(self._valueChanged)

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """
        Slot triggered when the model changes value.
        Updates value of the doublespinbox
        """
        if not self._rq_self_changing:
            self.setValue(float(self.model))

    _rq_self_changing = False
    """
    Flag to signal that this widget is triggering the update
    """

    @pyqtSlot()
    def _valueChanged(self) -> None:
        """
        Slot triggered when the user changes value of the doublespinbox.
        Propagates changes to the model
        """
        self._rq_self_changing = True
        self.model.set(self.value())
        self._rq_self_changing = False
