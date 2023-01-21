from typing import TYPE_CHECKING, Union

import pytest_cases

from pyreaqtive import RQInt, RQWidget, RQBool, RQFloat, RQText, RQLabel

from ..qtbot_window import window_fixture  # pylint: disable=unused-import

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("model", [
    RQInt(0),
    "Hello",
    True,
    6,
    6.2
])
@pytest_cases.parametrize('rq_if', [RQBool(False), RQBool(True), None])
@pytest_cases.parametrize('rq_disabled', [RQBool(False), RQBool(True), None])
def test_rqwidget(
        model: Union[RQInt, str, bool, int, float],
        rq_if: Union[RQBool, None],
        rq_disabled: Union[RQBool, None],
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name
) -> None:
    widget = RQWidget(
        model=model,
        rq_if=rq_if,
        rq_disabled=rq_disabled
    )

    if isinstance(model, RQInt):
        assert isinstance(widget.model, RQInt)
    elif model == "Hello":
        assert isinstance(widget.model, RQText)
        assert widget.model.get() == "Hello"
    elif model is True:
        assert isinstance(widget.model, RQBool)
        assert widget.model.get() is True
    elif model == 6:
        assert isinstance(widget.model, RQInt)
        assert widget.model.get() == 6
    elif model == 6.2:
        assert isinstance(widget.model, RQFloat)
        assert widget.model.get() == 6.2
    else:
        raise NotImplementedError

    widget = RQLabel(
        model=model,
        rq_if=rq_if,
        rq_disabled=rq_disabled
    )
    window_fixture.layout().addWidget(widget)
    window_fixture.show()

    if rq_if is not None:
        if rq_if:
            assert widget.isHidden() is False
            rq_if.set(False)
            assert widget.isHidden() is True
        else:
            assert widget.isHidden() is True
            rq_if.set(True)
            assert widget.isHidden() is False

    if rq_disabled is not None:
        if rq_disabled:
            assert widget.isEnabled() is False
            rq_disabled.set(False)
            assert widget.isEnabled() is True
        else:
            assert widget.isEnabled() is True
            rq_disabled.set(True)
            assert widget.isEnabled() is False
