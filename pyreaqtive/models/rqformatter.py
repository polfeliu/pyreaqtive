from .rqmodel import RQModel


class RQFormatter(RQModel):
    """Reactive text formatter

    Links to models and creates a string that is reactive to changes of models
    """

    def __init__(self, format_string: str, **kwargs):
        """Constructor

        Args:
            format_string: python formatting string

            kwargs: variables or reactive models in the format.
                Changes in these models will trigger rendering of the output string
        """
        super().__init__()
        self.format_string = format_string
        self.variables = kwargs
        for name, model in self.variables.items():
            if isinstance(model, RQModel) or issubclass(type(model), RQModel):
                model.rq_data_changed.connect(self._variable_changed)

    def _variable_changed(self) -> None:
        """Variable changed slot

        Called when some of the models have emitted _data_changed.
        Informs connected widgets that the formatter model has changed.
        Widgets will ask the string again and recalculate it with the new data
        """
        self.rq_data_changed.emit()

    def set(self, value) -> None:
        raise RuntimeError("RQFormatter does not allow set()")

    def get(self) -> str:
        """Get value of the model in string format

        Returns:
            str: formatted string with current model values
        """
        return self.format_string.format(
            **{key: str(variable) for key, variable in self.variables.items()}
        )

    def __str__(self) -> str:
        return self.get()
