from pyreaqtive import RQProgressBar, RQFloat, RQInt, RQObject
import pytest_cases

from .qtbot_window import window_fixture


@pytest_cases.parametrize("model", [
    RQInt(2),
    RQFloat(7.3),
    2,
    7.3,
    1007
])
def test_rqprogressbar(model, qtbot, window_fixture):
    widget = RQProgressBar(model)

    window_fixture.layout().addWidget(widget)
    window_fixture.show()

    if isinstance(model, RQInt):
        assert widget.value() == 2
    elif isinstance(model, RQFloat):
        assert widget.value() == 7  # Decimal places are removed
    elif model == 2:
        assert widget.value() == 2
    elif model == 7.3:
        assert widget.value() == 7
    elif model == 1007:
        assert widget.value() == -1
    else:
        raise NotImplementedError
