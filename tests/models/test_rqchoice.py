import pytest
import pytest_cases
from pyreaqtive import RQChoice, RQList
from enum import Enum, auto
from tests.signal_checker import *


@pytest_cases.parametrize("allow_none", [True, False])
@pytest_cases.parametrize("list_reactive", [True, False])
def test_choice_list(list_reactive: bool, allow_none: bool) -> None:
    choices = [
        'lorem',
        'ipsum',
        'dolor',
        4.6,
        object()
    ]

    if list_reactive:
        choices = RQList(choices)

    m = RQChoice(
        choices=choices,
        selected='lorem',
        allow_none=allow_none  # Correct selection
    )
    connect_signal(m.rq_data_changed)

    assert m[2] == choices[2]

    for i, item in enumerate(m):
        assert item == choices[i]

    with pytest.raises(IndexError):
        assert m[i + 1]

    assert m.get() == choices[0]
    assert str(m) == choices[0]

    with pytest.raises(KeyError):
        m = RQChoice(
            choices=choices,
            selected='asdf',  # Invalid selection
            allow_none=allow_none
        )

    if allow_none:
        m.set(None)
        assert_signal_emitted(m.rq_data_changed)
        assert m.selected == None
    else:
        with pytest.raises(ValueError):
            m.set(None)

    if allow_none:
        m = RQChoice(
            choices=choices,
            selected=None,
            allow_none=allow_none
        )

    assert m.get_choices() == choices

    m.reset()

    if allow_none:
        assert m.selected == None
    else:
        assert m.selected == choices[0]

    if list_reactive:
        m.set(choices[0])
        choices.__delitem__(0)

        if allow_none:
            m.selected = None
        else:
            m.selected = choices[0]


@pytest_cases.parametrize("allow_none", [True, False])
def test_choice_enum(allow_none: bool) -> None:
    class Choices(Enum):
        Lorem = auto()
        Ipsum = auto()
        Dolor = auto()

    class IncorrectChoice(Enum):
        Hello = auto()

    m = RQChoice(
        choices=Choices,
        selected=Choices.Dolor,
        allow_none=allow_none
    )
    connect_signal(m.rq_data_changed)

    assert m.selected == Choices.Dolor
    assert str(m) == "Choices.Dolor"

    if allow_none:
        m = RQChoice(
            choices=Choices,
            selected=None,
            allow_none=allow_none
        )
        connect_signal(m.rq_data_changed)

        assert m.selected == None
        assert str(m) == "None"

    else:
        with pytest.raises(ValueError):
            m = RQChoice(
                choices=Choices,
                selected=None,
                allow_none=allow_none
            )
            connect_signal(m.rq_data_changed)

    with pytest.raises(KeyError):
        m.set(IncorrectChoice.Hello)
        assert_signal_emitted(m.rq_data_changed)

    assert m.get_choices() == list(Choices)
