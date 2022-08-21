import pytest

from pyreaqtive import RQHBoxLayout, RQVBoxLayout, RQList
import pytest_cases
from qtpy.QtWidgets import QWidget

from ..qtbot_window import window_fixture


class ItemWidget(QWidget):

    def __init__(self, item: int, list_model: RQList):
        super().__init__()
        self.item = item


@pytest_cases.parametrize("layout_class", [RQHBoxLayout, RQVBoxLayout])
@pytest_cases.parametrize("widget_callback", [True, False])
@pytest_cases.parametrize("initial", [True, False])
def test_layouts(layout_class, widget_callback, initial, qtbot, window_fixture):
    if initial:
        list = RQList([1, 7, 3])
    else:
        list = RQList()

    if widget_callback:
        def widget(item: int, list_model: RQList):
            return ItemWidget(item, list_model)
    else:
        widget = ItemWidget

    layout = layout_class(
        model=list,
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

    list.insert(0, 2)
    if not initial:
        assert layout.count() == 1
        assert layout.itemAt(0).widget().item == 2
    else:
        assert layout.count() == 4
        assert layout.itemAt(0).widget().item == 2
        assert layout.itemAt(1).widget().item == 1
        assert layout.itemAt(2).widget().item == 7
        assert layout.itemAt(3).widget().item == 3

    list.append(95)
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

    list.remove_all(7)
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

    list.remove_all(2)
    if not initial:
        assert layout.count() == 1
        assert layout.itemAt(0).widget().item == 95
    else:
        assert layout.count() == 3
        assert layout.itemAt(0).widget().item == 1
        assert layout.itemAt(1).widget().item == 3
        assert layout.itemAt(2).widget().item == 95

    list.clear()
    assert layout.count() == 0
