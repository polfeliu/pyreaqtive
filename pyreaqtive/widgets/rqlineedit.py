from typing import TYPE_CHECKING, Union, Any

from qtpy.QtCore import Slot  # type: ignore
from qtpy.QtWidgets import QLineEdit  # type: ignore

from ..models import RQText, RQBool, RQObject, RQModel
from .rqwidget import RQWidget

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QLineEdit
    from PyQt5.QtCore import pyqtSlot as Slot


class RQLineEdit(RQWidget, QLineEdit):
    """Reactive LineEdit Widget."""

    model: Union[RQText, RQObject]
    """Model linked to the widget"""

    def __init__(self,
                 model: Union[RQText, str, RQObject],
                 *args: Any,
                 rq_if: Union[RQBool, None] = None,
                 rq_disabled: Union[RQBool, None] = None,
                 wait_for_finish: bool = False,
                 **kwargs: Any
                 ) -> None:
        """Constructor.

        Args:
            model: Model to link the widget to
            *args: arguments to pass to the native pyqt widget
            rq_if: RQBool that controls the visibility
            rq_disabled: RQBool that controls the disabling
            wait_for_finish: if true, the model is not updated until Enter is pressed or focus is changed
            **kwargs: arguments to pass to the native pyqt widget
        """
        if issubclass(type(model), RQModel):
            if model.rq_read_only:  # type: ignore
                raise IOError("Cannot connect rqlineedit to a read only model")

        RQWidget.__init__(self, model, rq_if, rq_disabled)
        QLineEdit.__init__(self, *args, **kwargs)
        self.rq_init_widget()

        self._rq_data_changed()
        self.model.rq_data_changed.connect(self._rq_data_changed)

        if wait_for_finish:
            self.editingFinished.connect(self._update_model)
        else:
            self.textChanged.connect(self._update_model)

    @Slot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the model changes text.

        Updates value of the LineEdit
        """
        if not self._rq_writing:
            self._rq_reading = True
            self.setText(str(self.model))
            self._rq_reading = False

    _rq_writing = False
    """Flag to signal that this widget is triggering the update and is writing to the model"""

    _rq_reading = False
    """Flag to indicate that the model changed and the widget is reading the model"""

    @Slot()
    def _update_model(self) -> None:
        """Propagates changes to the model."""
        if not self._rq_reading:
            self._rq_writing = True
            self.model.set(self.text())
            self._rq_writing = False
