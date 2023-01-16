from typing import Callable

import pytest
from tests.signal_checker import connect_signal, assert_signal_emitted

from pyreaqtive import RQModel, RQComputedModel, RQInt


def test_model() -> None:
    model = RQModel()
    connect_signal(model.rq_data_changed)
    connect_signal(model._rq_delete)  # pylint: disable=protected-access

    with pytest.raises(NotImplementedError):
        model.get()

    with pytest.raises(NotImplementedError):
        model.set(1)

    model.rq_data_changed.emit()
    assert_signal_emitted(model.rq_data_changed)

    model.__del__()  # pylint: disable=unnecessary-dunder-call
    assert_signal_emitted(model._rq_delete)  # pylint: disable=protected-access


def test_reactive_model() -> None:
    model1 = RQInt(2)
    model2 = RQInt(5)

    def callback(model1: int, model2: int) -> int:
        return model1 * model2

    with pytest.raises(TypeError):
        RQComputedModel(lambda: None)

    class TestRQModel(RQComputedModel, RQInt):
        def __init__(self, function: Callable, **kwargs: RQModel) -> None:
            RQInt.__init__(self, 0)
            RQComputedModel.__init__(self, function, **kwargs)

    model_computed = TestRQModel(
        callback,
        model1=model1,
        model2=model2
    )

    assert model_computed.rq_read_only is True
    assert model_computed.rq_computed_function == callback
    assert model_computed.rq_computed_variables['model1'] == model1
    assert model_computed.rq_computed_variables['model2'] == model2

    assert model_computed.get() == 10

    with pytest.raises(RuntimeError):
        model_computed.set(1)

    model1.set(1)
    assert model_computed.get() == 5

    model1.set(10)
    model2.set(10)
    assert model_computed.get() == 100
