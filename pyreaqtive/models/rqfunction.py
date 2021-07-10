from .rqmodel import RQModel


class RQFunction(RQModel):
    def __init__(self, function, **kwargs):
        super().__init__()
        self.function = function
        self.variables = kwargs
        for name, model in self.variables.items():
            if isinstance(model, RQModel) or issubclass(type(model), RQModel):
                model._rq_data_changed.connect(self._variable_changed)

    def _variable_changed(self):
        self._rq_data_changed.emit()

    def __float__(self):
        return self.function(
            **{key: float(variable) for key, variable in self.variables.items()}
        )

    def __str__(self):
        return str(self.__float__())
