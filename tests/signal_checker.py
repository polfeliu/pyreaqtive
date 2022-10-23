from typing import Dict, Union

from qtpy.QtCore import Signal  # type: ignore

triggered: Dict[Signal, Union[bool, int]] = {

}


def connect_signal(signal: Signal) -> None:
    triggered[signal] = False

    def callback() -> None:
        triggered[signal] = True

    signal.connect(callback)


def connect_int_signal(signal: Signal) -> None:
    triggered[signal] = False

    def callback(value: int) -> None:
        triggered[signal] = value

    signal.connect(callback)


def disconnect_signal(signal: Signal) -> None:
    del triggered[signal]


def assert_signal_emitted(signal: Signal) -> None:
    assert triggered[signal] is True
    triggered[signal] = False


def assert_int_signal(signal: Signal, value: int) -> None:
    assert triggered[signal] == value
    triggered[signal] = False
