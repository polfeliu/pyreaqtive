from typing import TYPE_CHECKING, Union

from qtpy.QtCore import Slot  # type: ignore
from qtpy.QtWidgets import QPushButton  # type: ignore

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QPushButton

from ..models import RQBool, RQModel

from .rqwidget import RQWidget


class RQPushButton(RQWidget, QPushButton):
    """Reactive PushButton Widget"""

    def __init__(self,
                 model: Union[RQModel, str],
                 *args,
                 rq_if: Union[RQBool, None] = None,
                 rq_disabled: Union[RQBool, None] = None,
                 **kwargs):
        """Constructor.

        Args:
            model: Model to link the widget to
            *args: arguments to pass to the native pyqt widget
            rq_if: RQBool that controls the visibility
            rq_disabled: RQBool that controls the disabling
            **kwargs: arguments to pass to the native pyqt widget
        """
        RQWidget.__init__(self, model, rq_if=rq_if, rq_disabled=rq_disabled)
        QPushButton.__init__(self, str(model), *args, **kwargs)
        self.rq_init_widget()

        self.model.rq_data_changed.connect(self._rq_data_changed)

    @Slot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the pushbutton text
        """
        self.setText(str(self.model))
