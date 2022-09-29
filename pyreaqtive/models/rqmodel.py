from typing import TYPE_CHECKING, Any, Callable

from qtpy.QtCore import QObject, Signal, Slot  # type: ignore

if TYPE_CHECKING:
    from PyQt5.QtCore import QObject
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtCore import pyqtSlot as Slot


class RQModel(QObject):
    """RQModel Base Class.

    All pyreaqtive models must inherit from this class, that provides basic get, set method and data changed signals
    """

    rq_read_only = False
    """Indicates if the model cannot be written to. Set() raises error"""

    rq_data_changed = Signal()
    """Data changed signal.

    Widgets that are connected to models can connect slots to this signal.
    The model must emit to this when the state of it changes, to notify the widgets.
    """

    _rq_delete = Signal()
    """Delete signal.

    Signals that the model instance is about to be deleted
    """

    def get(self) -> Any:
        """Method to get the value of the underlying object.

        Must be overridden by model

        Returns:
            Any: value of the object
        """
        raise NotImplementedError

    def set(self, value: Any) -> None:
        """Method to set the value of the underlying object.

        Must be overridden by model

        Args:
            value: New value of the model
        """
        raise NotImplementedError

    def __del__(self) -> None:
        try:
            self._rq_delete.emit()
        except RuntimeError:  # pragma: no cover
            # If object has been deleted ignore this error
            pass


class RQComputedModel:
    """RQComputedModel Base Class.

    All pyreaqtive computed models must inherit from this class.
    Computed models are those that are calculated from others values, by means of a function.
    Changes in the linked models trigger events that updates linked widgets, than in turn calculate the function.
    """

    def __init__(self, function: Callable, **kwargs: RQModel):
        """Constructor.

        Args:
            function: function to calculate the model value from input values

            **kwargs: reactive models in the function by variable name as keyword
                Changes in these models will trigger recalculation of the function
        """
        if not issubclass(type(self), RQModel):
            raise TypeError("RQComputed models must inherit from RQModel by the parent class")

        self.rq_read_only = True
        self.rq_computed_function: Callable = function
        self.rq_computed_variables: dict = kwargs
        for _, model in self.rq_computed_variables.items():
            model.rq_data_changed.connect(self._variable_changed)

        # First calculation
        self._variable_changed()

    @Slot()
    def _variable_changed(self) -> None:
        """Variable changed slot.

        Called when some of the models have emitted rq_data_changed.
        Informs connected widgets that the function model has changed.
        Widgets will ask the value again and recalculate it with the new data
        """
        # RQModels have rq_data_changed, asserted on __init__
        self.rq_data_changed.emit()  # type: ignore

    def set(self, value: Any) -> None:
        raise RuntimeError("Computed Models do not allow set()")

    def get(self) -> Any:
        """Get value of the model in the output format of the function.

        Returns:
            function result with current model values
        """
        return self.rq_computed_function(
            **{key: variable.get() for key, variable in self.rq_computed_variables.items()}
        )
