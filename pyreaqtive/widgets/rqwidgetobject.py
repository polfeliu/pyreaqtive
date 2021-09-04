import gc

from PyQt5.QtWidgets import QCheckBox, QLayout, QLabel
from PyQt5.QtCore import pyqtSlot, QObject

from ..models import RQBool
from .rqwidget import RQWidget
from typing import Union, Callable


class RQWidgetObject(RQWidget, QObject):

    def __init__(self, model, layout: QLayout, widget: Callable):
        RQWidget.__init__(self, model)
        QObject.__init__(self)
        self.layout = layout
        if not hasattr(self.layout, "rq_widget_object"):
            self.layout.rq_widget_objects = []
        self.layout.rq_widget_objects = self
        self.widget_callback = widget  # TODO Allow the same typing and callbacks as lists widgets
        self.model.rq_data_changed.connect(self._rq_data_changed)
        self.new_widget()
        self.layout.addWidget(self.widget)

    def new_widget(self):
        self.widget = self.widget_callback(self.model.get())
        return self.widget

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        index = self.layout.indexOf(self.widget)
        self.layout.removeWidget(self.widget)
        self.new_widget()
        self.layout.insertWidget(index, self.widget)

    def show(self):
        pass

    def hide(self):
        pass
