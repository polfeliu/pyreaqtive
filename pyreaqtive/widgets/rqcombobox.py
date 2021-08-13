from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSlot

from ..models import RQChoice


class RQCombobox(QComboBox):
    """Reactive ComboBox Widget"""

    model: RQChoice
    """Model linked to the widget"""

    def __init__(self, model: RQChoice, *args, **kwargs):
        """Constructor

        Args:
            model: Model to link the widget to

            args: arguments to pass to the native pyqt combobox widget
            kwargs: arguments to pass to the native pyqt combobox widget
        """
        super().__init__(*args, **kwargs)
        self.model = model
        self.model._rq_data_changed.connect(self._rq_data_changed)
        self.model._choices._rq_list_insert.connect(self._rq_choice_insert)
        self.model._choices._rq_list_remove.connect(self._rq_choice_remove)

        for index, choice in enumerate(self.model._choices):
            self._rq_choice_insert(index)

        if self.model.allow_none:
            self.addItem("None")

        self.currentIndexChanged.connect(self._current_index_changed)

        self._rq_data_changed()

    @pyqtSlot(int)
    def _rq_choice_insert(self, index: int) -> None:
        """Slot triggered when the list of choices inserts a new item.

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
        """Slot triggered when the list of choices removes a new item

        Removes the option from the combobox

        Args:
            index: element of the list
        """
        self.removeItem(index)

    @pyqtSlot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the selection of the choice model changed

        Updates the combobox selection
        """
        if not self._rq_writing:
            self._rq_reading = True
            if self.model._selected is not None:
                self.setCurrentIndex(
                    self.model._choices.get_index(
                        self.model._selected
                    )
                )
            else:
                self.setCurrentIndex(
                    self.count() - 1
                )
            self._rq_reading = False

    _rq_writing = False
    """Flag to signal that this widget is triggering the update and is writing to the model"""

    _rq_reading = False
    """Flag to indicate that the model changed and the widget is reading the model"""

    @pyqtSlot(int)
    def _current_index_changed(self, index: int) -> None:
        """Slot triggered when the user changes the selection in the combobox

        Args:
            index: selected item index
        """
        if not self._rq_reading:
            self._rq_writing = True

            if self.model.allow_none and self.currentIndex() == self.count() - 1:
                choice = None
            else:
                choice = self.model._choices.get_item(index)

            self.model.set(choice)

            self._rq_writing = False
