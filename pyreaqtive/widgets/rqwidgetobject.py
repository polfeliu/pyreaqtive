from typing import Union, Callable, Type

from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QLayout, QWidget

from .rqwidget import RQWidget
from ..models import RQObject


class RQWidgetObject(RQWidget, QObject):
    """Reactive Widget Object

    Displays a widget for a RQObject.
    If the instance of the RQObject changes, the widget is destroyed and a new one is created in the same place
    """

    model: RQObject
    """Model linked to the widget"""

    def __init__(self, model: RQObject, layout: QLayout, widget: Union[Type[QWidget], Callable[[object], QWidget]]):
        """Constructor

        Args:
            model: Model to link the widget to
            layout: layout to place the widget
            widget: QWidget type that represents each the instances
                Can also be a function that accepts the instance as argument, and returns the widget instance
        """
        RQWidget.__init__(self, model)
        QObject.__init__(self)
        self.layout = layout
        if not hasattr(self.layout, "rq_widget_object"):
            self.layout.rq_widget_objects = []
        self.layout.rq_widget_objects = self
        if issubclass(widget, QWidget):
            self.rq_widget_callback = lambda instance: widget(instance)
        else:
            self.rq_widget_callback = widget
        self.model.rq_data_changed.connect(self._rq_data_changed)
        self._rq_new_widget()
        self.layout.addWidget(self.widget)

    def _rq_new_widget(self) -> QWidget:
        """Generate a new widget from the model"""
        self.widget = self.rq_widget_callback(self.model.get())
        return self.widget

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when when model has changed

        Deletes widget from the layout and adds the new one in the same place
        """
        index = self.layout.indexOf(self.widget)
        self.layout.removeWidget(self.widget)
        self._rq_new_widget()
        self.layout.insertWidget(index, self.widget)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()
