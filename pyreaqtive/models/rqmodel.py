from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from typing import Any, Callable


class RQModel(QObject):
    """RQModel Base Class.

    All pyreaqtive models must inherit from this class, that provides basic get, set method and data changed signals
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

    rq_data_changed = pyqtSignal()
    """pyqtSignal data changed signal.
    
    Widgets that are connected to models can connect slots to this signal.
    The model must emit to this when the state of it changes, to notify the widgets.
    """

    _rq_delete = pyqtSignal()
    """pyqtSignal delete signal.
    
    Signals that the model instance is about to be deleted
    """

    def __delete__(self):
        self._rq_delete.emit()


class RQComputedModel(RQModel):
    """RQComputedModel Base Class.

    All pyreaqtive computed models must inherit from this class.
    Computed models are those that are calculated from others values, by means of a function.
    Changes in the linked models trigger events that updates linked widgets, than in turn calculate the function.
    """

    def __init__(self, function: Callable, **kwargs):
        """Constructor

        Args:
            function: function to calculate the model value from input values

            kwargs: reactive models in the function by variable name as keyword
                Changes in these models will trigger recalculation of the function
        """
        RQModel.__init__(self)
        self.rq_computed_function = function
        self.rq_computed_variables = kwargs
        for name, model in self.rq_computed_variables.items():
            if isinstance(model, RQModel) or issubclass(type(model), RQModel):
                model.rq_data_changed.connect(self._variable_changed)

    @pyqtSlot()
    def _variable_changed(self) -> None:
        """Variable changed slot

        Called when some of the models have emitted rq_data_changed.
        Informs connected widgets that the function model has changed.
        Widgets will ask the value again and recalculate it with the new data
        """
        self.rq_data_changed.emit()

    def set(self, value) -> None:
        raise RuntimeError("Computed Models do not allow set()")

    def get(self):
        """Get value of the model in the output format of the function

        Returns:
            function result with current model values
        """
        return self.rq_computed_function(
            **{key: variable.get() for key, variable in self.rq_computed_variables.items()}
        )
