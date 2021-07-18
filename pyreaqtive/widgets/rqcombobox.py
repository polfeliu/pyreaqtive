from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..models import RQChoice


class RQCombobox(QComboBox):
    """
    Reactive ComboBox Widget
    """

    model: RQChoice
    """
    Model linked to the widget
    """

    def __init__(self, model: RQChoice, *args):
        """
        Args:
            model: Model to link the widget to

            *args: arguments to pass to the native pyqt combobox widget
        """
        super().__init__(*args)
        self.model = model
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.model._choices._rq_list_insert.connect(self._rq_choice_insert)
        self.model._choices._rq_list_remove.connect(self._rq_choice_remove)

        for index, choice in enumerate(self.model._choices):
            self._rq_choice_insert(index)

        self.currentIndexChanged.connect(self._currentIndexChanged)

    @pyqtSlot(int)
    def _rq_choice_insert(self, index: int) -> None:
        """
        Slot triggered when the list of choices inserts a new item.
        Adds the option to the combobox

        Args:
            index: element of the list
        """
        self.insertItem(
            index,
            str(self.model._choices.get_item(index))
        )

    @pyqtSlot(int)
    def _rq_choice_remove(self, index: int) -> None:
        """
        Slot triggered when the list of choices removes a new item
        Removes the option from the combobox

        Args:
            index: element of the list
        """
        self.removeItem(index)

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """
        Slot triggered when the selection of the choice model changed.
        Updates the combobox selection
        """
        if not self._rq_self_changing:
            self.setCurrentIndex(
                self.model._choices.get_index(
                    self.model._selected
                )
            )
            pass

    _rq_self_changing = False
    """
    Flag to signal that this widget is triggering the update
    """

    @pyqtSlot(int)
    def _currentIndexChanged(self, index: int) -> None:
        """
        Slot triggered when the user changes the selection in the combobox

        Args:
            index: selected item index
        """
        self._rq_self_changing = True
        self.model.set(
            self.model._choices.get_item(index)
        )
        self._rq_self_changing = False
