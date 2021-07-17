from .rqmodel import RQModel


class RQFormatter(RQModel):
    """
    Reactive text formatter

    Links to models and creates a string that is reactive to changes of models
    """

    def __init__(self, format_string: str, **kwargs):
        """
        Args:
            format_string: python formatting string
            **kwargs: list of variables or reactive models in the format
                Changes in this list of models will trigger the rendering of the output string
        """
        super().__init__()
        self.format_string = format_string
        self.variables = kwargs
        for name, model in self.variables.items():
            if isinstance(model, RQModel) or issubclass(type(model), RQModel):
                model._rq_data_changed.connect(self._variable_changed)

    def _variable_changed(self):
        self._rq_data_changed.emit()

    def __str__(self):
        return self.format_string.format(
            **{key: str(variable) for key, variable in self.variables.items()}
        )
