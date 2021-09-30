from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSlot

from ..models import RQInt, RQFloat, RQBool, RQObject
from typing import Union

from .rqwidget import RQWidget


class RQPushButton(RQWidget, QPushButton):
    """Reactive PushButton Widget"""

    def __init__(self, *args, rq_if: Union[RQBool, None] = None, rq_disabled: Union[RQBool, None] = None, **kwargs):
        """Constructor.

        Args:
            model: Model to link the widget to
            args: arguments to pass to the native pyqt widget
            rq_if: RQBool that controls the visibility
            rq_disabled: RQBool that controls the disabling

            **kwargs: arguments to pass to the native pyqt widget
        """
        RQWidget.__init__(self, model=None, rq_if=rq_if, rq_disabled=rq_disabled)
        QPushButton.__init__(self, *args, **kwargs)
        self.rq_init_widget()