from .rqmodel import RQModel


class RQFormatter(RQModel):
    def __init__(self, format_string, **kwargs):
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
