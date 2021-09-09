from typing import Union

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QProgressBar

from ..models import RQInt, RQFloat, RQBool, RQObject
from .rqwidget import RQWidget


class RQProgressBar(RQWidget, QProgressBar):
    """Reactive ProgressBar Widget"""

    model: Union[RQInt, RQFloat, RQObject]
    """Model linked to the widget"""

    def __init__(self, model: Union[RQInt, RQFloat, int, float, RQObject], *args, rq_if: Union[RQBool, None] = None,
                 **kwargs):
        """Constructor.

        Args:
            model: Model to link the widget to

            args: arguments to pass to the native pyqt widget

            rq_if: RQBool that controls the visibility

            **kwargs: arguments to pass to the native pyqt widget
        """
        RQWidget.__init__(self, model, rq_if)
        QProgressBar.__init__(self, *args, **kwargs)

        self.model.rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the progressbar
        """
        self.setValue(self.model.get())
