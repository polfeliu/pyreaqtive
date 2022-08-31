from typing import TYPE_CHECKING, Callable, Type, Union, Any

from qtpy.QtWidgets import QBoxLayout, QWidget  # type: ignore

from .rqboxlayout import RQBoxLayout
from ..models import RQList

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QBoxLayout, QWidget


class RQVBoxLayout(RQBoxLayout):
    """Reactive QVBoxLayout."""

    def __init__(self,
                 model: RQList,
                 widget: Union[Type[QWidget], Callable[[Any, RQList], QWidget]],
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        """Constructor.

        Args:
            model: RQList representing all the items in the layout

            widget: QWidget type that represents each item.
                Can also be a function that accepts the item and list model as arguments,
                and returns the widget instance

            args: arguments to pass to the native pyqt layout

            **kwargs: arguments to pass to the native pyqt layout
        """
        super().__init__(model, widget, QBoxLayout.Down, *args, **kwargs)
