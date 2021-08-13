from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSlot

from ..models import RQModel


class RQLabel(QLabel):
    """Reactive Label Widget"""

    model: RQModel = None
    """Model linked to the widget"""

    def __init__(self, model: RQModel, *args, **kwargs):
        """Constructor.

        Args:
            model: Model to link the widget to

            args: arguments to pass to the native pyqt label widget
            kwargs: arguments to pass to the native pyqt label widget
        """
        super().__init__(str(self.model), *args, **kwargs)
        self.model = model
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the dial
        """
        self.setText(str(self.model))
