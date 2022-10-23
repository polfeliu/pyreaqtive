from typing import TYPE_CHECKING, Union

import pytest_cases
import pytest

from pyreaqtive import RQFloat, RQInt, RQDial, RQComputedInt

from ..qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("model", [
    RQInt(2),
    RQFloat(7.3),
    2,
    7.3,
    1007,
    -6
])
def test_rqdial(
        model: Union[RQInt, RQFloat, int, float],
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name
) -> None:
    widget_1 = RQDial(model)
    window_fixture.layout().addWidget(widget_1)

    if isinstance(model, (RQInt, RQFloat)):
        widget_2 = RQDial(model)
        window_fixture.layout().addWidget(widget_2)

    window_fixture.show()

    if isinstance(model, RQInt):
        assert widget_1.value() == 2
    elif isinstance(model, RQFloat):
        assert widget_1.value() == 7  # Decimal places are removed
    elif model == 2:
        assert widget_1.value() == 2
    elif model == 7.3:
        assert widget_1.value() == 7
    elif model == 1007:
        assert widget_1.value() == 99
    elif model == -6:
        assert widget_1.value() == 0
    else:
        raise NotImplementedError

    widget_1.setValue(70)
    assert widget_1.value() == 70

    if isinstance(model, (RQInt, RQFloat)):
        assert widget_2.value() == 70
        widget_2.setValue(30)
        assert widget_1.value() == 30
        assert widget_2.value() == 30


def test_rqdial_readonly(
        qtbot: 'QtBot'  # pylint: disable=unused-argument
) -> None:
    model = RQComputedInt(
        lambda: 1
    )

    with pytest.raises(IOError):
        model = RQDial(model)
