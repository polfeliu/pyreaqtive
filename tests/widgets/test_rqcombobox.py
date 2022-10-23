from typing import TYPE_CHECKING

import pytest

from pyreaqtive import RQChoice, RQCombobox, RQList

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore


def test_rqcombobox_rqchoice(qtbot: 'QtBot') -> None:
    choices = RQList([1, 2, 4])
    selection = RQChoice(
        choices=choices,
        selected=4
    )

    combobox = RQCombobox(model=selection)

    assert [int(combobox.itemText(i)) for i in range(combobox.count())] == [1, 2, 4]
    assert combobox.currentText() == '4'

    choices.insert(1, 3)
    assert [int(combobox.itemText(i)) for i in range(combobox.count())] == [1, 3, 2, 4]

    selection.set(2)
    assert combobox.currentText() == '2'

    choices.remove(2)
    assert combobox.currentText() == '1'

    with pytest.raises(ValueError):
        selection.set(None)

    selection._allow_none = True
    combobox = RQCombobox(model=selection)
    selection.set(None)
    assert combobox.currentText() == 'None'

    selection.set(1)
    assert combobox.currentText() == '1'
    choices.remove(1)
    assert combobox.currentText() == 'None'

    # Non reactive list
    selection.rq_choices_list = [1, 2, 3]
    combobox = RQCombobox(model=selection)

    # Futurible read only testing
    selection.rq_read_only = True
    with pytest.raises(IOError):
        RQCombobox(model=selection)

#  RQ IF
#  RQ DISABLED
