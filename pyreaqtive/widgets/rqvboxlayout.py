from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQModel, RQList
from .rqwidget import RQWidget

from typing import List, Dict, Callable, Type


class RQVBoxLayout(QVBoxLayout):
    model: RQList
    widget_callback: Callable[[Type[RQModel]], Type[QWidget]]

    def __init__(self, model: RQList, widget_callback: Callable[[Type[RQModel]], QWidget], *args):
        super().__init__(*args)
        self.model = model
        self.widget_callback = widget_callback

        if not isinstance(model, RQList):
            raise TypeError
        else:
            self.model._rq_list_insert.connect(self._rq_insert_widget)
            self.model._rq_list_remove.connect(self._rq_remove_widget)

        for index, item in enumerate(self.model._list):
            self._rq_insert_widget(index)

    widgets: List[QWidget] = []

    @pyqtSlot(int)
    def _rq_insert_widget(self, index):
        model = self.model.get_item(index)
        self.widgets.insert(index, self.widget_callback(model))
        self.addWidget(self.widgets[index])

    @pyqtSlot(int)
    def _rq_remove_widget(self, index):
        self.removeWidget(self.widgets[index])
        self.widgets[index].deleteLater()
        self.widgets.pop(index)
