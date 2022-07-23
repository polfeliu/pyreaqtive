from pyreaqtive import RQText, RQComputedText
import pytest_cases
from tests.signal_checker import *


def test_text():
    m = RQText("Hello")
    connect_signal(m.rq_data_changed)

    assert m._text == "Hello"
    assert m.get() == "Hello"
    assert str(m) == "Hello"

    m.set("Hello World")
    assert_signal_emitted(m.rq_data_changed)
    assert m._text == "Hello World"
    assert m.get() == "Hello World"
    assert str(m) == "Hello World"


def test_computed_text():
    m1 = RQText()
    m2 = RQText()

    mc = RQComputedText(
        lambda m1, m2: m1 + m2,
        m1=m1,
        m2=m2
    )
    connect_signal(mc.rq_data_changed)

    assert mc.get() == ""

    m1.set("Hello")
    assert_signal_emitted(mc.rq_data_changed)
    assert mc.get() == "Hello"

    m2.set(" World")
    assert_signal_emitted(mc.rq_data_changed)
    assert mc.get() == "Hello World"


def test_computed_text_format():
    m1 = RQText("Hello")
    m2 = RQText("World")

    mc = RQComputedText(
        "{m1} {m2}!",
        m1=m1,
        m2=m2
    )
    connect_signal(mc.rq_data_changed)

    assert mc.get() == "Hello World!"

    m2.set("Mars")
    assert_signal_emitted(mc.rq_data_changed)
    assert mc.get() == "Hello Mars!"
