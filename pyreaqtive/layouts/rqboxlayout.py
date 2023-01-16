from typing import TYPE_CHECKING, List, Callable, Type, Union, Any

from qtpy.QtCore import Slot  # type: ignore
from qtpy.QtWidgets import QBoxLayout, QWidget  # type: ignore

from ..models import RQList

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QBoxLayout, QWidget
    from PyQt5.QtCore import pyqtSlot as Slot


class RQBoxLayout(QBoxLayout):
    """Reactive QBoxLayout."""

    def __init__(self,
                 model: RQList,
                 widget: Union[Type[QWidget], Callable[[Any, RQList], QWidget]],
                 *args: Any,
                 **kwargs: Any
                 ):
        """Constructor.

        Args:
            model: RQList representing all the items in the layout

            widget: QWidget type that represents each item.
                The constructor of the widget must take as arguments: object (Object) and list (RQList).
                Can also be a function that accepts the item and list model as arguments,
                and returns the widget instance

            args: arguments to pass to the native pyqt layout

            **kwargs: arguments to pass to the native pyqt layout
        """
        super().__init__(*args, **kwargs)
        self.model: RQList = model
        """Model linked to the layout"""

        self.widgets: List[QWidget] = []
        """List of current widgets in the layout"""

        self._rq_widget_callback: Callable[[Any, RQList], QWidget]
        """Widget callback. For a new object that is insert on the list, must return the new and appropriate widget"""

        if not hasattr(widget, "inherits"):
            # Not a QWidget
            def callback(item: Any, list_model: RQList) -> QWidget:
                return widget(item, list_model)

            self._rq_widget_callback = callback
        else:
            self._rq_widget_callback = widget

        self.model.rq_list_insert.connect(self._rq_insert_widget)
        self.model.rq_list_remove.connect(self._rq_remove_widget)

        for index, _ in enumerate(self.model):
            self._rq_insert_widget(index)

    @Slot(int)
    def _rq_insert_widget(self, index: int) -> None:
        """Slot triggered when the model inserts a new item.

        Args:
            index: index in the initial of the new instance
        """
        item = self.model[index]
        self.widgets.insert(index, self._rq_widget_callback(item, self.model))
        self.insertWidget(index, self.widgets[index])

    @Slot(int)
    def _rq_remove_widget(self, index: int) -> None:
        """Slot triggered when the model removes an item.

        Args:
            index: index in the list of the item removal
        """
        self.removeWidget(self.widgets[index])
        self.widgets[index].deleteLater()
        self.widgets.pop(index)
