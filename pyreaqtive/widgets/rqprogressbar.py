from typing import Union

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QProgressBar

from ..models import RQInt, RQFloat


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

        self.model.rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the progressbar
        """
        self.setValue(self.model.get())
