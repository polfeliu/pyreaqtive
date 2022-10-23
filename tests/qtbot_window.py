from typing import TYPE_CHECKING

import pytest

from PyQt5.QtWidgets import QMainWindow

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore


@pytest.fixture()
def window_fixture(
        qtbot: 'QtBot'  # pylint: disable=unused-argument
) -> QMainWindow:
    window = QMainWindow()
    qtbot.addWidget(window)

    return window
