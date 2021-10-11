from typing import Callable, Type, Union, Any

from PyQt5.QtWidgets import QBoxLayout, QWidget

from .rqboxlayout import RQBoxLayout
from ..models import RQList


class RQVBoxLayout(RQBoxLayout):
    """Reactive QVBoxLayout"""

    def __init__(self, model: RQList,
                 widget: Union[Type[QWidget], Callable[[Any, RQList], QWidget]], *args, **kwargs):
        """Constructor

        Args:
            model: RQList representing all the items in the layout

            widget: QWidget type that represents each item.
                Can also be a function that accepts the item and list model as arguments,
                and returns the widget instance

            args: arguments to pass to the native pyqt layout

            **kwargs: arguments to pass to the native pyqt layout
        """
        super().__init__(model, widget, QBoxLayout.Direction.Down, *args, **kwargs)
