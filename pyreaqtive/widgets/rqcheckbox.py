from typing import Union

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QCheckBox

from .rqwidget import RQWidget
from ..models import RQBool, RQModel


class RQCheckbox(RQWidget, QCheckBox):
    """Reactive Checkbox Widget"""

    model: RQBool
    """Model linked to the widget"""

    def __init__(self,
                 model: Union[RQBool, bool],
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
            **kwargs: arguments to pass to the native pyqt widget
        """
        if isinstance(type(model), RQModel):
            if model.rq_read_only:  # type: ignore
                raise IOError("Cannot connect rqcheckbox to a read only model")

        RQWidget.__init__(self, model, rq_if, rq_disabled)
        QCheckBox.__init__(self, *args, **kwargs)
        self.rq_init_widget()

        self.toggled.connect(self._toggled)
        self.model.rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes state.

        Updates the state of the checkbox
        """
        if not self._rq_writing:
            self._rq_reading = True
            self.setChecked(bool(self.model))
            self._rq_reading = False

    _rq_writing = False
    """Flag to signal that this widget is triggering the update and is writing to the model"""

    _rq_reading = False
    """Flag to indicate that the model changed and the widget is reading the model"""

    @pyqtSlot()
    def _toggled(self) -> None:
        """Slot triggered when the user changes state of this checkbox.

        Propagates changes to the model
        """
        if not self._rq_reading:
            self._rq_writing = True
            self.model.set(bool(self.checkState()))
            self._rq_writing = False
