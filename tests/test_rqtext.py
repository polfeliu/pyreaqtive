from pyreaqtive import RQText, RQComputedText
import pytest_cases


def test_text():
    m = RQText("Hello")
    assert m._text == "Hello"
    assert m.get() == "Hello"
    assert str(m) == "Hello"

    m.set("Hello World")
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

    assert mc.get() == ""

    m1.set("Hello")
    assert mc.get() == "Hello"

    m2.set(" World")
    assert mc.get() == "Hello World"


def test_computed_text_format():
    m1 = RQText("Hello")
    m2 = RQText("World")

    mc = RQComputedText(
        "{m1} {m2}!",
        m1=m1,
        m2=m2
    )

    assert mc.get() == "Hello World!"

    m2.set("Mars")

    assert mc.get() == "Hello Mars!"
