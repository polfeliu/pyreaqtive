from typing import TYPE_CHECKING
from enum import Enum, auto

import pytest_cases

from pyreaqtive import RQFloat, RQConnect

from .qtbot_window import window_fixture  # pylint: disable=unused-import


class Conversion(Enum):
    CONVERSION = auto()
    LINEAR_CONVERSION = auto()


if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot  # type: ignore
    from PyQt5.QtWidgets import QMainWindow


@pytest_cases.parametrize("conversion", [Conversion.CONVERSION, Conversion.LINEAR_CONVERSION])
def test_rqconnect(
        conversion: Conversion,
        qtbot: 'QtBot',  # pylint: disable=unused-argument
        window_fixture: 'QMainWindow'  # pylint: disable=redefined-outer-name, unused-argument)
) -> None:
    celsius = RQFloat(1)
    fahrenheit = RQFloat(1)

    if conversion == Conversion.CONVERSION:
        connect = RQConnect(  # pylint: disable=unused-variable
            model_a=celsius,  # Connect to model A
            model_b=fahrenheit,  # Connect to Model B
            conversion=RQConnect.Conversion(  # Declare conversion formulas to convert reciprocally
                a_to_b=lambda c: c * (9 / 5) + 32,
                b_to_a=lambda f: (f - 32) / (9 / 5)
            )
        )
    elif conversion == Conversion.LINEAR_CONVERSION:
        connect = RQConnect(  # pylint: disable=unused-variable
            model_a=celsius,
            model_b=fahrenheit,
            conversion=RQConnect.LinearConversion(
                scale_a_to_b=9 / 5,
                offset_a_to_b=32
            )
        )
    else:
        raise NotImplementedError

    celsius.set(2)
    assert int(fahrenheit.get()) == 35

    fahrenheit.set(40)
    assert int(celsius.get()) == 4
