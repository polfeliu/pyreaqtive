from pyreaqtive import RQProgressBar, RQFloat, RQInt, RQComputedInt, RQSlider
import pytest_cases
import pytest
from time import sleep
from .qtbot_window import window_fixture


@pytest_cases.parametrize("model", [
    RQInt(2),
    RQFloat(7.3),
    2,
    7.3,
    1007,
    -6
])
def test_rqslider(model, qtbot, window_fixture):
    widget_1 = RQSlider(model)
    window_fixture.layout().addWidget(widget_1)

    if isinstance(model, RQInt) or isinstance(model, RQFloat):
        widget_2 = RQSlider(model)
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

    if isinstance(model, RQInt) or isinstance(model, RQFloat):
        assert widget_2.value() == 70
        widget_2.setValue(30)
        assert widget_1.value() == 30
        assert widget_2.value() == 30


def test_rqslider_readonly(qtbot):
    m = RQComputedInt(
        lambda: 1
    )

    with pytest.raises(IOError):
        m = RQSlider(m)
