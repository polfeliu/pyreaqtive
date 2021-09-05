from PyQt5.QtWidgets import QBoxLayout, QWidget
from PyQt5.QtCore import pyqtSlot

from ..models import RQModel, RQList

from typing import List, Callable, Type, Union


class RQBoxLayout(QBoxLayout):
    """Reactive QBoxLayout"""

    def __init__(self, model: RQList,
                 widget: Union[Type[QWidget], Callable[[RQModel, RQList], QWidget]], *args,
                 **kwargs):
        """Constructor

        Args:
            model: RQList representing all the items in the layout

            widget: QWidget type that represents each item.
                The constructor of the widget must take as arguments: model (RQModel) and list (RQList).
                Can also be a function that accepts the item model and list model as arguments,
                and returns the widget instance

            args: arguments to pass to the native pyqt layout

            kwargs: arguments to pass to the native pyqt layout
        """
        super().__init__(*args, **kwargs)
        self.model: RQList = model
        """Model linked to the layout"""

        self.widgets: List[QWidget] = []
        """List of current widgets in the layout"""

        self._rq_widget_callback: Callable[[RQModel, RQList], QWidget]
        """Widget callback. For a new model that is insert on the list, must return the new and appropriate widget"""

        if issubclass(widget, QWidget):
            self._rq_widget_callback = lambda item_model, list_model: widget(item_model, list_model)
        elif callable(widget):
            self._rq_widget_callback = widget
        else:
            raise TypeError

        if not isinstance(model, RQList):
            raise TypeError
        else:
            self.model.rq_list_insert.connect(self._rq_insert_widget)
            self.model.rq_list_remove.connect(self._rq_remove_widget)

        for index, item in enumerate(self.model):
            self._rq_insert_widget(index)

    @pyqtSlot(int)
    def _rq_insert_widget(self, index) -> None:
        """Slot triggered when the model inserts a new item

        Args:
            index: index in the initial of the new instance
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
