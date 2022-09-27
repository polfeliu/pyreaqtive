from typing import TYPE_CHECKING, Union, Any

from qtpy.QtCore import Slot  # type: ignore
from qtpy.QtWidgets import QComboBox  # type: ignore

from .rqwidget import RQWidget
from ..models import RQChoice, RQBool, RQList

if TYPE_CHECKING:
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtWidgets import QComboBox


class RQComboBox(RQWidget, QComboBox):
    """Reactive ComboBox Widget."""

    model: RQChoice
    """Model linked to the widget"""

    def __init__(self,
                 model: RQChoice,
                 *args: Any,
                 rq_if: Union[RQBool, None] = None,
                 rq_disabled: Union[RQBool, None] = None,
                 **kwargs: Any
                 ) -> None:
        """Constructor.

        Args:
            model: Model to link the widget to
            *args: arguments to pass to the native pyqt widget
            rq_if: RQBool that controls the visibility
            rq_disabled: RQBool that controls the disabling
            **kwargs: arguments to pass to the native pyqt widget
        """
        if model.rq_read_only:
            raise IOError("Cannot connect rqcombobox to a read only model")

        RQWidget.__init__(self, model, rq_if, rq_disabled)
        QComboBox.__init__(self, *args, **kwargs)
        self.rq_init_widget()

        self.model.rq_data_changed.connect(self._rq_data_changed)
        if isinstance(self.model.rq_choices_list, RQList):
            self.model.rq_choices_list.rq_list_insert.connect(self._rq_choice_insert)
            self.model.rq_choices_list.rq_list_remove.connect(self._rq_choice_remove)

        for index, _ in enumerate(self.model):
            self._rq_choice_insert(index)

        if self.model._allow_none:
            self.addItem("None")

        self.currentIndexChanged.connect(self._current_index_changed)

        self._rq_data_changed()

    @Slot(int)
    def _rq_choice_insert(self, index: int) -> None:
        """Slot triggered when the initial of choices inserts a new item.

        Adds the option to the combobox

        Args:
            index: element of the initial
        """
        self.insertItem(
            index,
            str(self.model[index])
        )

    @Slot(int)
    def _rq_choice_remove(self, index: int) -> None:
        """Slot triggered when the initial of choices removes a new item.

        Removes the option from the combobox

        Args:
            index: element of the initial
        """
        self.removeItem(index)

    @Slot()
    def _rq_data_changed(self) -> None:
        """Slot triggered when the selection of the choice model changed.

        Updates the combobox selection
        """
        if not self._rq_writing:
            self._rq_reading = True
            if self.model.selected is not None:
                self.setCurrentIndex(
                    self.model.get_choices().index(
                        self.model.selected
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

    @Slot(int)
    def _current_index_changed(self, index: int) -> None:
        """Slot triggered when the user changes the selection in the combobox.

        Args:
            index: selected item index
        """
        if not self._rq_reading:
            self._rq_writing = True

            if self.model._allow_none and self.currentIndex() == self.count() - 1:  # pylint: disable=protected-access
                choice = None
            else:
                choice = self.model[index]

            self.model.set(choice)

            self._rq_writing = False
