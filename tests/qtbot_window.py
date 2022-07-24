import pytest

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


@pytest.fixture()
def window_fixture(qtbot):
    window = QMainWindow()
    qtbot.addWidget(window)


    return window
