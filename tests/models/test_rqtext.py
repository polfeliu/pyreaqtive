from tests.signal_checker import connect_signal, assert_signal_emitted

from pyreaqtive import RQText, RQComputedText


def test_text() -> None:
    model = RQText("Hello")
    connect_signal(model.rq_data_changed)

    assert model._text == "Hello"  # pylint: disable=protected-access
    assert model.get() == "Hello"
    assert str(model) == "Hello"

    model.set("Hello World")
    assert_signal_emitted(model.rq_data_changed)
    assert model._text == "Hello World"  # pylint: disable=protected-access
    assert model.get() == "Hello World"
    assert str(model) == "Hello World"


def test_computed_text() -> None:
    model1 = RQText()
    model2 = RQText()

    model_computed = RQComputedText(
        lambda m1, m2: m1 + m2,
        m1=model1,
        m2=model2
    )
    connect_signal(model_computed.rq_data_changed)

    assert model_computed.get() == ""

    model1.set("Hello")
    assert_signal_emitted(model_computed.rq_data_changed)
    assert model_computed.get() == "Hello"

    model2.set(" World")
    assert_signal_emitted(model_computed.rq_data_changed)
    assert model_computed.get() == "Hello World"


def test_computed_text_format() -> None:
    model1 = RQText("Hello")
    model2 = RQText("World")

    model_computed = RQComputedText(
        "{m1} {m2}!",
        m1=model1,
        m2=model2
    )
    connect_signal(model_computed.rq_data_changed)

    assert model_computed.get() == "Hello World!"

    model2.set("Mars")
    assert_signal_emitted(model_computed.rq_data_changed)
    assert model_computed.get() == "Hello Mars!"
