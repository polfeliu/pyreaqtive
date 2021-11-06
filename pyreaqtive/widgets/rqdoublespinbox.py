from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtCore import pyqtSlot

from ..models import RQFloat, RQBool, RQObject
from .rqwidget import RQWidget

from typing import Union


class RQDoubleSpinBox(RQWidget, QDoubleSpinBox):
    """Reactive DoubleSpinBox Widget"""

    model: Union[RQFloat, RQObject]
    """Model linked to the widget"""

    def __init__(self,
                 model: Union[RQFloat, float, RQObject],
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
        if isinstance(model, RQFloat):
            if model.rq_read_only:
                raise IOError("Cannot connect rqdoublespinbox to a read only model")

        RQWidget.__init__(self, model, rq_if, rq_disabled)
        QDoubleSpinBox.__init__(self, *args, **kwargs)
        self.rq_init_widget()

        self._rq_data_changed()
        self.model.rq_data_changed.connect(self._rq_data_changed)
        self.valueChanged.connect(self._value_changed)

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes value.

        Updates value of the doublespinbox
        """
        if not self._rq_writing:
            self._rq_reading = True
            self.setValue(float(self.model))
            self._rq_reading = False

    _rq_writing = False
    """Flag to signal that this widget is triggering the update and is writing to the model"""

    _rq_reading = False
    """Flag to indicate that the model changed and the widget is reading the model"""

    @pyqtSlot()
    def _value_changed(self) -> None:
        """Slot triggered when the user changes value of the doublespinbox.

        Propagates changes to the model
        """
        if not self._rq_reading:
            self._rq_writing = True
            self.model.set(self.value())
            self._rq_writing = False
