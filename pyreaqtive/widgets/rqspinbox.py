from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import pyqtSlot

from ..models import RQInt


class RQSpinBox(QSpinBox):
    """Reactive SpinBox Widget"""

    model: RQInt = None
    """Model linked to the widget"""

    def __init__(self, model: RQInt, *args):
        """Constructor.

        Args:
            model: Model to link the widget to

            args: arguments to pass to the native pyqt spinbox widget

            kwargs: arguments to pass to the native pyqt spinbox widget
        """
        super().__init__(*args)
        self.model = model
        self._rq_data_changed()
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.valueChanged.connect(self._value_changed)

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the spinbox
        """
        if not self._rq_writing:
            self._rq_reading = True
            self.setValue(int(self.model))
            self._rq_reading = False

    _rq_writing = False
    """Flag to signal that this widget is triggering the update and is writing to the model"""

    _rq_reading = False
    """Flag to indicate that the model changed and the widget is reading the model"""

    @pyqtSlot()
    def _value_changed(self) -> None:
        """Slot triggered when the user changes value of the spinbox.

        Propagates changes to the model
        """
        if not self._rq_reading:
            self._rq_writing = True
            self.model.set(self.value())
            self._rq_writing = False
