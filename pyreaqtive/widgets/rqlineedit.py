from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQText


class RQLineEdit(QLineEdit):
    """
    Reactive LineEdit Widget
    """

    model: RQText
    """
    Model linked to the widget
    """

    def __init__(self, model: RQText, *args):
        """
        Args:
            model: Model to link the widget to

            \*args: arguments to pass to the native pyqt LineEdit widget
        """
        self.model = model
        super().__init__(*args)
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.textChanged.connect(self._valueChanged)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """
        Slot triggered when the model changes text
        Updates value of the LineEdit
        """
        if not self._rq_self_changing:
            self.setText(str(self.model))

    _rq_self_changing = False
    """
    Flag to signal that this widget is triggering the update
    """

    @pyqtSlot(str)
    def _valueChanged(self, text: str) -> None:
        """
        Slot triggered when the user changes text of the LineEdit
        Propagates changes to the model
        """
        self._rq_self_changing = True
        self.model.set(text)
        self._rq_self_changing = False
