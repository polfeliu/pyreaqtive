from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSlot

from ..models import RQModel, RQList

from typing import List, Callable, Type, Union


class RQVBoxLayout(QVBoxLayout):
    """Reactive QVBoxLayout"""

    model: RQList
    """Model linked to the layout"""

    _rq_widget_callback: Callable[[RQModel, RQList], QWidget]
    """
    Widget callback. For a new model that is insert on the list, must return the new and appropriate widget
    """

    def __init__(self, model: RQList,
                 widget: Union[Type[QWidget], Callable[[RQModel, RQList], QWidget]], *args, **kwargs):
        """Constructor

        Args:
            model: RQList representing all the items in the layout

            widget: QWidget type that represents each item.
                Can also be a function that accepts the item model and list model as arguments,
                and returns the widget instance

            args: arguments to pass to the native pyqt label widget
            kwargs: arguments to pass to the native pyqt label widget
        """
        super().__init__(*args, **kwargs)
        self.model = model

        self.widgets: List[QWidget] = []

        if isinstance(widget, QWidget):
            self._rq_widget_callback = lambda item_model, list_model: widget(item_model, list_model)
        elif callable(widget):
            self._rq_widget_callback = widget
        else:
            raise TypeError

        if not isinstance(model, RQList):
            raise TypeError
        else:
            self.model._rq_list_insert.connect(self._rq_insert_widget)
            self.model._rq_list_remove.connect(self._rq_remove_widget)

        for index, item in enumerate(self.model._list):
            self._rq_insert_widget(index)

    @pyqtSlot(int)
    def _rq_insert_widget(self, index) -> None:
        """Slot triggered when the model inserts a new item

        Args:
            index: index in the list of the new instance
        """
        item_model = self.model[index]
        self.widgets.insert(index, self._rq_widget_callback(item_model, self.model))
        self.insertWidget(index, self.widgets[index])

    @pyqtSlot(int)
    def _rq_remove_widget(self, index) -> None:
        """Slot triggered when the model removes a new item

        Args:
            index: index in the list of the item removal
        """
        self.removeWidget(self.widgets[index])
        self.widgets[index].deleteLater()
        self.widgets.pop(index)
