from .rqmodel import RQModel


class RQBool(RQModel):
    _bool: bool

    def __init__(self, state):
        """
        :param state:
        """
        super().__init__()
        self._bool = state

    def get(self):
        """
        get method
        :return:
        """
        return self._bool

    def set(self, value):
        """
        set method
        :param value:
        :return:
        """
        self._bool = value
        self._rq_data_changed.emit()

    def toggle(self):
        """
        toggle method
        :return:
        """
        self.set(not self.get())

    def __bool__(self):
        """
        bool value of rqbool
        :return:
        """
        return self._bool
