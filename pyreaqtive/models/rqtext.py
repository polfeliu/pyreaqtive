from .rqmodel import RQModel

class RQText(RQModel):

    _text: str

    def __init__(self, text):
        super().__init__()
        self._text = text

    def get(self):
        return self._text

    def set(self, value):
        self._text = value
        self._rq_data_changed.emit()

    def __str__(self):
        return self._text