from typing import TYPE_CHECKING, Union

from pyreaqtive import RQInt, RQWidget, RQBool, RQFloat, RQText, RQLabel
import pytest_cases

from ..qtbot_window import window_fixture

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
def test_rqwidget(model: Union[RQInt, str, bool, int, float], rq_if: Union[RQBool, None],
                  rq_disabled: Union[RQBool, None], qtbot: 'QtBot',
                  window_fixture: 'QMainWindow') -> None:
    w = RQWidget(
        model=model,
        rq_if=rq_if,
        rq_disabled=rq_disabled
    )

    if isinstance(model, RQInt):
        assert isinstance(w.model, RQInt)
    elif model == "Hello":
        assert isinstance(w.model, RQText)
        assert w.model.get() == "Hello"
    elif model is True:
        assert isinstance(w.model, RQBool)
        assert w.model.get() == True
    elif model == 6:
        assert isinstance(w.model, RQInt)
        assert w.model.get() == 6
    elif model == 6.2:
        assert isinstance(w.model, RQFloat)
        assert w.model.get() == 6.2
    else:
        raise NotImplementedError

    w = RQLabel(
        model=model,
        rq_if=rq_if,
        rq_disabled=rq_disabled
    )
    window_fixture.layout().addWidget(w)
    window_fixture.show()

    if rq_if is not None:
        if rq_if:
            assert w.isHidden() is False
            rq_if.set(False)
            assert w.isHidden() is True
        else:
            assert w.isHidden() is True
            rq_if.set(True)
            assert w.isHidden() is False

    if rq_disabled is not None:
        if rq_disabled:
            assert w.isEnabled() is False
            rq_disabled.set(False)
            assert w.isEnabled() is True
        else:
            assert w.isEnabled() is True
            rq_disabled.set(True)
            assert w.isEnabled() is False
