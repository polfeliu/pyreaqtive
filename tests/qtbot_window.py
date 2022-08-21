from typing import TYPE_CHECKING

import pytest

from qtpy.QtWidgets import *

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow


@pytest.fixture()
def window_fixture(qtbot):
    window = QMainWindow()
    qtbot.addWidget(window)

    return window
