from enum import Enum, auto

import pytest
import pytest_cases

from pyreaqtive import RQChoice, RQList
from tests.signal_checker import connect_signal, assert_signal_emitted


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

    model = RQChoice(
        choices=choices,
        selected='lorem',
        allow_none=allow_none  # Correct selection
    )
    connect_signal(model.rq_data_changed)

    assert model[2] == choices[2]

    for i, item in enumerate(model):
        assert item == choices[i]

    with pytest.raises(IndexError):
        assert model[len(model) + 1]

    assert model.get() == choices[0]
    assert str(model) == choices[0]

    with pytest.raises(KeyError):
        model = RQChoice(
            choices=choices,
            selected='asdf',  # Invalid selection
            allow_none=allow_none
        )

    if allow_none:
        model.set(None)
        assert_signal_emitted(model.rq_data_changed)
        assert model.selected is None
    else:
        with pytest.raises(ValueError):
            model.set(None)

    if allow_none:
        model = RQChoice(
            choices=choices,
            selected=None,
            allow_none=allow_none
        )

    assert model.get_choices() == choices

    model.reset()

    if allow_none:
        assert model.selected is None
    else:
        assert model.selected == choices[0]

    if list_reactive:
        model.set(choices[0])
        choices.__delitem__(0)  # pylint: disable=unnecessary-dunder-call

        if allow_none:
            model.selected = None
        else:
            model.selected = choices[0]


@pytest_cases.parametrize("allow_none", [True, False])
def test_choice_enum(allow_none: bool) -> None:
    class Choices(Enum):
        LOREM = auto()
        IPSUM = auto()
        DOLOR = auto()

    class IncorrectChoice(Enum):
        HELLO = auto()

    model = RQChoice(
        choices=Choices,
        selected=Choices.DOLOR,
        allow_none=allow_none
    )
    connect_signal(model.rq_data_changed)

    assert model.selected == Choices.DOLOR
    assert str(model) == "Choices.DOLOR"

    if allow_none:
        model = RQChoice(
            choices=Choices,
            selected=None,
            allow_none=allow_none
        )
        connect_signal(model.rq_data_changed)

        assert model.selected is None
        assert str(model) == "None"

    else:
        with pytest.raises(ValueError):
            model = RQChoice(
                choices=Choices,
                selected=None,
                allow_none=allow_none
            )
            connect_signal(model.rq_data_changed)

    with pytest.raises(KeyError):
        model.set(IncorrectChoice.HELLO)
        assert_signal_emitted(model.rq_data_changed)

    assert model.get_choices() == list(Choices)
