from typing import TYPE_CHECKING
from PyQt5.QtWidgets import QWidget

import pytest_cases

from pyreaqtive import RQBoxLayout, RQHBoxLayout, RQVBoxLayout, RQList

from ..qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


class ItemWidget(QWidget):

    def __init__(self, item: int, list_model: RQList):
        super().__init__()
        self.item = item
        self.list_model = list_model


@pytest_cases.parametrize("layout_class", [RQHBoxLayout, RQVBoxLayout])
@pytest_cases.parametrize("widget_callback", [True, False])
@pytest_cases.parametrize("initial", [True, False])
def test_layouts(
        layout_class: RQBoxLayout,
        widget_callback: bool,
        initial: bool,
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name
) -> None:
    if initial:
        lst = RQList([1, 7, 3])
    else:
        lst = RQList()

    if widget_callback:
        def widget(item: int, list_model: RQList) -> ItemWidget:
            return ItemWidget(item, list_model)
    else:
        widget = ItemWidget

    layout = layout_class(
        model=lst,
        widget=widget
    )
    main_widget = QWidget()
    window_fixture.layout().addWidget(main_widget)
    main_widget.setLayout(layout)
    window_fixture.show()

    if not initial:
        assert layout.count() == 0
    else:
        assert layout.count() == 3
        assert layout.itemAt(0).widget().item == 1
        assert layout.itemAt(1).widget().item == 7
        assert layout.itemAt(2).widget().item == 3

    lst.insert(0, 2)
    if not initial:
        assert layout.count() == 1
        assert layout.itemAt(0).widget().item == 2
    else:
        assert layout.count() == 4
        assert layout.itemAt(0).widget().item == 2
        assert layout.itemAt(1).widget().item == 1
        assert layout.itemAt(2).widget().item == 7
        assert layout.itemAt(3).widget().item == 3

    lst.append(95)
    if not initial:
        assert layout.count() == 2
        assert layout.itemAt(0).widget().item == 2
        assert layout.itemAt(1).widget().item == 95
    else:
        assert layout.count() == 5
        assert layout.itemAt(0).widget().item == 2
        assert layout.itemAt(1).widget().item == 1
        assert layout.itemAt(2).widget().item == 7
        assert layout.itemAt(3).widget().item == 3
        assert layout.itemAt(4).widget().item == 95

    lst.remove_all(7)
    if not initial:
        assert layout.count() == 2
        assert layout.itemAt(0).widget().item == 2
        assert layout.itemAt(1).widget().item == 95
    else:
        assert layout.count() == 4
        assert layout.itemAt(0).widget().item == 2
        assert layout.itemAt(1).widget().item == 1
        assert layout.itemAt(2).widget().item == 3
        assert layout.itemAt(3).widget().item == 95

    lst.remove_all(2)
    if not initial:
        assert layout.count() == 1
        assert layout.itemAt(0).widget().item == 95
    else:
        assert layout.count() == 3
        assert layout.itemAt(0).widget().item == 1
        assert layout.itemAt(1).widget().item == 3
        assert layout.itemAt(2).widget().item == 95

    lst.clear()
    assert layout.count() == 0
