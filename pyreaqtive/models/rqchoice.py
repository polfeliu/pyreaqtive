from .rqmodel import RQModel
from .rqlist import RQList

from typing import List, Union

class RQChoice(RQModel):

    _choices: RQList
    _selected: Union[RQModel, None]

    def __init__(self, choices: RQList, selected:RQModel= None):
        super().__init__()
        self._choices = choices
        self._selected = selected
        # TODO Validate selected

    def get(self):
        return self._selected

    def get_choices(self):
        return self._choices

    def set(self, value):
        self._selected = value
        #self.validate_selected()
        self._rq_data_changed.emit()

    def __str__(self):
        return self._selected