from typing import TYPE_CHECKING, Union

from qtpy.QtWidgets import QWidget  # type: ignore

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget

from ..models import RQModel, RQText, RQBool, RQInt, RQFloat, RQObject


class RQWidget:
    """Reactive Widget Base class"""

    def __init__(self,
                 model: Union[RQModel, str, bool, int, float, RQObject, None],
                 rq_if: Union[RQBool, None] = None,
                 rq_disabled: Union[RQBool, None] = None
                 ):
        """Constructor.

        This class always always inherits from QWidget but is not declared as so. User defined widgets,
        will directly have the QWidget methods

        Args:
            model: model to link the widget to. Can also be a built-in type that is converted to a dummy model
            rq_if: RQBool that controls the visibility
            rq_disabled: RQBool that controls the disabling
        """

        if isinstance(model, str):
            model = RQText(model)
        elif isinstance(model, int):
            model = RQInt(model)
        elif isinstance(model, float):
            model = RQFloat(model)
        elif isinstance(model, bool):
            model = RQBool(model)

        self.model = model

        self._rq_if_model = rq_if
        self._rq_disabled_model = rq_disabled

    def rq_init_widget(self):
        if self._rq_if_model is not None:
            self._rq_if_model.rq_data_changed.connect(self._rq_if_data_changed)
            self._rq_if_data_changed()
        if self._rq_disabled_model is not None:
            self._rq_disabled_model.rq_data_changed.connect(self._rq_disabled_data_changed)
            self._rq_disabled_data_changed()

    def _rq_if_data_changed(self) -> None:
        if issubclass(type(self), QWidget):
            if self._rq_if_model:
                self.show()  # type: ignore
            else:
                self.hide()  # type: ignore

    def _rq_disabled_data_changed(self) -> None:
        if issubclass(type(self), QWidget):
            self.setDisabled(bool(self._rq_disabled_model))  # type: ignore
