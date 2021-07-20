from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQInt, RQFloat
from typing import Union

class RQSlider(QSlider):
    """
    Reactive Slider Widget
    """

    model: Union[RQInt, RQFloat]
    """
    Model linked to the widget
    """

    def __init__(self, model: Union[RQInt, RQFloat], *args):
        """
        Args:
            model: Model to link the widget to

            \*args: arguments to pass to the native pyqt slider widget
        """
        super().__init__(*args)
        self.model = model
        self._rq_data_changed()
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.valueChanged.connect(self._valueChanged)

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """
        Slot triggered when the model changes value.
        Updates value of the slider
        """
        if not self._rq_self_changing:
            self.setValue(int(self.model))

    _rq_self_changing = False
    """
    Flag to signal that this widget is triggering the update
    """

    @pyqtSlot()
    def _valueChanged(self) -> None:
        """
        Slot triggered when the user changes value of the slider.
        Propagates changes to the model
        """
        self._rq_self_changing = True
        self.model.set(self.value())
        self._rq_self_changing = False
