from typing import TYPE_CHECKING, Union, Any

from qtpy.QtCore import Slot  # type: ignore
from qtpy.QtWidgets import QProgressBar  # type: ignore

from .rqwidget import RQWidget
from ..models import RQInt, RQFloat, RQBool, RQObject

if TYPE_CHECKING:
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtWidgets import QProgressBar


class RQProgressBar(RQWidget, QProgressBar):
    """Reactive ProgressBar Widget."""

    model: Union[RQInt, RQFloat, RQObject]
    """Model linked to the widget."""

    def __init__(self,
                 model: Union[RQInt, RQFloat, int, float, RQObject],
                 *args: Any,
                 rq_if: Union[RQBool, None] = None,
                 rq_disabled: Union[RQBool, None] = None,
                 **kwargs: Any
                 ) -> None:
        """Constructor.

        Args:
            model: Model to link the widget to
            *args: arguments to pass to the native pyqt widget
            rq_if: RQBool that controls the visibility
            rq_disabled: RQBool that controls the disabling
            **kwargs: arguments to pass to the native pyqt widget
        """
        RQWidget.__init__(self, model, rq_if, rq_disabled)
        QProgressBar.__init__(self, *args, **kwargs)
        self.rq_init_widget()

        self.model.rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @Slot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the progressbar
        """
        self.setValue(int(self.model))
