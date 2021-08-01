from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQBool


class RQCheckbox(QCheckBox):
    """
    Reactive Checkbox Widget
    """

    model: RQBool
    """
    Model linked to the widget 
    """

    def __init__(self, model: RQBool, *args):
        """
        Args:
            model: Model to link the widget to

            \*args: arguments to pass to the native pyqt checkbox widget
        """
        super().__init__(*args)
        self.model = model
        self.toggled.connect(self._toggled)
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self._rq_data_changed()

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """
        Slot triggered when the model changes state.
        Updates the state of the checkbox
        """
        if not self._rq_self_changing:
            self._rq_being_changed = True
            self.setChecked(bool(self.model))
            self._rq_being_changed = False

    _rq_self_changing = False
    """
    Flag to signal that this widget is triggering the update
    """

    _rq_being_changed = False
    """
    Flag to indicate if the widget is being changed from the model
    """

    @pyqtSlot()
    def _toggled(self) -> None:
        """
        Slot triggered when the user changes state of this checkbox.
        Propagates changes to the model
        """
        if not self._rq_being_changed:
            self._rq_self_changing = True
            self.model.set(bool(self.checkState()))
            self._rq_self_changing = False
