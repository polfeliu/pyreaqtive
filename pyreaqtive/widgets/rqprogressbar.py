from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQInt, RQFloat
from typing import Union


class RQProgressBar(QProgressBar):
    """Reactive ProgressBar Widget"""

    model: Union[RQInt, RQFloat]
    """Model linked to the widget"""

    def __init__(self, model: Union[RQInt, RQFloat], *args, **kwargs):
        """Constructor

        Args:
            model: Model to link the widget to

            args: arguments to pass to the native pyqt progressbar widget
            kwargs: arguments to pass to the native pyqt progressbar widget
        """
        self.model = model
        super().__init__(*args, **kwargs)

        self.model._rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the progressbar
        """
        self.setValue(self.model.get())
