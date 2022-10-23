from typing import TYPE_CHECKING

import pytest

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore


@pytest.fixture()
def window_fixture(qtbot: 'QtBot') -> QMainWindow:
    window = QMainWindow()
    qtbot.addWidget(window)

    return window
