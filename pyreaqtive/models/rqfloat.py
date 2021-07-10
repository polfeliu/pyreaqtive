from .rqmodel import RQModel

class RQFloat(RQModel):

    _float: float

    def __init__(self, initial_float: float):
        super().__init__()
        self._float = initial_float

    def get(self):
        return self._float

    def set(self, value):
        self._float = value
        self._rq_data_changed.emit()

    def __str__(self):
        return str(self._float)

    def __int__(self):
        return int(self._float)

    def __float__(self):
        return self._float
