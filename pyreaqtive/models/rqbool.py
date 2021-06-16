from .rqmodel import RQModel

class RQBool(RQModel):

    _bool: bool

    def __init__(self, state):
        super().__init__()
        self._bool = state

    def get(self):
        return self._bool

    def set(self, value):
        self._bool = value
        self._rq_data_changed.emit()

    def toggle(self):
        self.set(not self.get())

    def __bool__(self):
        return self._bool