from typing import TYPE_CHECKING, Union, Callable, Type

from qtpy.QtCore import QObject  # type: ignore
from qtpy.QtCore import Slot
from qtpy.QtWidgets import QWidget  # type: ignore

from .rqwidget import RQWidget
from ..models import RQObject

if TYPE_CHECKING:
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtCore import QObject
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout


class RQWidgetObject(RQWidget, QObject):
    """Reactive Widget Object.

    Displays a widget for a RQObject.
    If the instance of the RQObject changes, the widget is destroyed and a new one is created in the same place
    """

    model: RQObject
    """Model linked to the widget"""

    def __init__(self,
                 model: RQObject,
                 layout: Union['QHBoxLayout', 'QVBoxLayout'],
                 widget: Union[Type[QWidget], Callable[[object], QWidget]]
                 ) -> None:
        """Constructor.

        Args:
            model: Model to link the widget to
            layout: layout to place the widget
            widget: QWidget type that represents each the instances
                Can also be a function that accepts the instance as argument, and returns the widget instance
        """
        RQWidget.__init__(self, model)
        QObject.__init__(self)
        self.rq_init_widget()

        self.layout = layout
        if not hasattr(self.layout, "rq_widget_objects"):
            self.layout.rq_widget_objects = []  # type: ignore
        self.layout.rq_widget_objects = self  # type: ignore
        self.rq_widget_callback = widget

        self.model.rq_data_changed.connect(self._rq_data_changed)
        self._rq_new_widget()
        self.layout.addWidget(self.widget)

    def _rq_new_widget(self) -> QWidget:
        """Generate a new widget from the model."""
        self.widget = self.rq_widget_callback(self.model.get())
        return self.widget

    @Slot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when model has changed.

        Deletes widget from the layout and adds the new one in the same place
        """
        index = self.layout.indexOf(self.widget)
        self.layout.removeWidget(self.widget)
        self.widget.deleteLater()
        self._rq_new_widget()
        self.layout.insertWidget(index, self.widget)

    def show(self) -> None:
        self.widget.show()

    def hide(self) -> None:
        self.widget.hide()
