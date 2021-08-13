from .rqmodel import RQModel
from typing import Callable


class RQFunction(RQModel):
    """Reactive mathematical function

    Links to models and creates a mathematical result that is reactive to changes of models
    """

    def __init__(self, function: Callable, **kwargs):
        """Constructor

        Args:
            function: mathematical function

            kwargs: variables or reactive models in the function
                Changes in these models will trigger recalculation of the function
        """
        super().__init__()
        self.function = function
        self.variables = kwargs
        for name, model in self.variables.items():
            if isinstance(model, RQModel) or issubclass(type(model), RQModel):
                model._rq_data_changed.connect(self._variable_changed)

    def _variable_changed(self) -> None:
        """Variable changed slot

        Called when some of the models have emitted _data_changed.
        Informs connected widgets that the function model has changed.
        Widgets will ask the string again and recalculate it with the new data
        """
        self._rq_data_changed.emit()

    def set(self, value) -> None:
        raise RuntimeError("RQFunction does not allow set()")

    def get(self) -> float:
        """Get value of the model in float format

        Returns:
            float: function result with current model values
        """
        return self.function(
            **{key: float(variable) for key, variable in self.variables.items()}
        )

    def __float__(self) -> float:
        return self.get()

    def __str__(self) -> str:
        """Get value of the model in string format

        Returns:
            str: function result with current model values converted to string
        """
        return str(self.__float__())
