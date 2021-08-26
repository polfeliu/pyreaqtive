from PyQt5.QtWidgets import QBoxLayout, QWidget
from .rqboxlayout import RQBoxLayout

from ..models import RQModel, RQList
from typing import List, Callable, Type, Union


class RQVBoxLayout(RQBoxLayout):
    """Reactive QVBoxLayout"""

    def __init__(self, model: RQList,
                 widget: Union[Type[QWidget], Callable[[RQModel, RQList], QWidget]], *args, **kwargs):
        super().__init__(model, widget, QBoxLayout.Direction.Down, *args, **kwargs)
