from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQChoice


class RQCombobox(QComboBox):
    model: RQChoice

    def __init__(self, model, *args):
        super().__init__(*args)
        self.model = model
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.model._choices._rq_list_insert.connect(self._rq_choice_insert)
        self.model._choices._rq_list_remove.connect(self._rq_choice_remove)

        for index, choice in enumerate(self.model._choices):
            self._rq_choice_insert(index)

        self.currentIndexChanged.connect(self._currentIndexChanged)

    @pyqtSlot(int)
    def _rq_choice_insert(self, index):
        self.insertItem(
            index,
            str(self.model._choices.get_item(index))
        )

    @pyqtSlot(int)
    def _rq_choice_remove(self, index):
        self.removeItem(index)

    @pyqtSlot()
    def _rq_data_changed(self):
        if not self._rq_self_changing:
            self.setCurrentIndex(
                self.model._choices.get_index(
                    self.model._selected
                )
            )
            pass

    _rq_self_changing = False

    @pyqtSlot(int)
    def _currentIndexChanged(self, index):
        self._rq_self_changing = True
        self.model.set(
            self.model._choices.get_item(index)
        )
        self._rq_self_changing = False
