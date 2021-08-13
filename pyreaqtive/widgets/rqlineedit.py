from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSlot

from ..models import RQText


class RQLineEdit(QLineEdit):
    """Reactive LineEdit Widget"""

    model: RQText
    """Model linked to the widget"""

    def __init__(self, model: RQText, *args, **kwargs):
        """Constructor

        Args:
            model: Model to link the widget to

            args: arguments to pass to the native pyqt LineEdit widget
            kwargs: arguments to pass to the native pyqt LineEdit widget
        """
        self.model = model
        super().__init__(*args, **kwargs)
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.textChanged.connect(self._valueChanged)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes text.

        Updates value of the LineEdit
        """
        if not self._rq_writing:
            self._rq_reading = True
            self.setText(str(self.model))
            self._rq_reading = False

    _rq_writing = False
    """Flag to signal that this widget is triggering the update and is writing to the model"""

    _rq_reading = False
    """Flag to indicate that the model changed and the widget is reading the model"""

    @pyqtSlot(str)
    def _valueChanged(self, text: str) -> None:
        """Slot triggered when the user changes text of the LineEdit.

        Propagates changes to the model
        """
        if not self._rq_reading:
            self._rq_writing = True
            self.model.set(text)
            self._rq_writing = False
