from pyreaqtive import RQFloat, RQDoubleSpinBox, RQConnect
import pytest_cases
from enum import Enum, auto
from .qtbot_window import window_fixture


class Conversion(Enum):
    Conversion = auto()
    LinearConversion = auto()


@pytest_cases.parametrize("conversion", [Conversion.Conversion, Conversion.LinearConversion])
def test_rqconnect(conversion, qtbot, window_fixture):
    celsius = RQFloat(1)
    fahrenheit = RQFloat(1)

    celsius_spinbox = RQDoubleSpinBox(celsius)
    fahrenheit_spinbox = RQDoubleSpinBox(fahrenheit)

    if conversion == Conversion.Conversion:
        connect = RQConnect(
            model_a=celsius,  # Connect to model A
            model_b=fahrenheit,  # Connect to Model B
            conversion=RQConnect.Conversion(  # Declare conversion formulas to convert reciprocally
                a_to_b=lambda c: c * (9 / 5) + 32,
                b_to_a=lambda f: (f - 32) / (9 / 5)
            )
        )
    elif conversion == Conversion.LinearConversion:
        connect = RQConnect(
            model_a=celsius,
            model_b=fahrenheit,
            conversion=RQConnect.LinearConversion(
                scale_a_to_b=9 / 5,
                offset_a_to_b=32
            )
        )
    else:
        raise NotImplemented

    celsius.set(2)
    assert int(fahrenheit.get()) == 35

    fahrenheit.set(40)
    assert int(celsius.get()) == 4
