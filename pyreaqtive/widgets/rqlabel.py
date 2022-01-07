from typing import Union

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel

from .rqwidget import RQWidget
from ..models import RQModel, RQBool, RQObject


class RQLabel(RQWidget, QLabel):
    """Reactive Label Widget"""

    model: RQModel
    """Model linked to the widget"""

    def __init__(self,
                 model: Union[RQModel, str, RQObject],
                 *args,
                 rq_if: Union[RQBool, None] = None,
                 rq_disabled: Union[RQBool, None] = None,
                 **kwargs
                 ):
        """Constructor.

        Args:
            model: Model to link the widget to
            *args: arguments to pass to the native pyqt widget
            rq_if: RQBool that controls the visibility
            rq_disabled: RQBool that controls the disabling
            **kwargs: arguments to pass to the native pyqt widget
        """
        RQWidget.__init__(self, model, rq_if, rq_disabled)
        QLabel.__init__(self, str(self.model), *args, **kwargs)
        self.rq_init_widget()

        self.model.rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the dial
        """
        self.setText(str(self.model))
