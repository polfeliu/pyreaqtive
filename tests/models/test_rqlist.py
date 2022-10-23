from typing import Any, Union

import pytest
from tests.signal_checker import connect_signal, assert_signal_emitted, assert_int_signal, connect_int_signal

from pyreaqtive import RQList, RQModel, RQInt, RQComputedList


def test_init() -> None:
    initial = [1, 6, 4]
    model = RQList(initial_items=initial)

    assert model._list == initial  # pylint: disable=protected-access

    model = RQList()
    assert model._list == []  # pylint: disable=protected-access


def test_del() -> None:
    model = RQList([8, 4, 5])

    connect_signal(model.rq_data_changed)
    connect_int_signal(model.rq_list_remove)
    del model[1]
    assert_int_signal(model.rq_list_remove, 1)
    assert list(model) == [8, 5]

    model.pop()
    assert_signal_emitted(model.rq_data_changed)
    assert_int_signal(model.rq_list_remove, 1)
    assert list(model) == [8]
    model.pop()
    assert_signal_emitted(model.rq_data_changed)
    assert_int_signal(model.rq_list_remove, 0)
    assert len(list(model)) == 0


@pytest.mark.parametrize(
    "start, stop, step",
    [
        (1, 3, None),
        (1, 6, 2),
        (-1, 2, None),
        (-1, 5, 3)
    ])
def test_del_slice(start: int, stop: int, step: Union[int, None]) -> None:
    lst = [8, 4, 5, 6, 7, 3, 7, 5]
    model = RQList(lst)

    connect_signal(model.rq_data_changed)
    connect_int_signal(model.rq_list_remove)
    if step is None:
        del model[start:stop]
        del lst[start:stop]
    else:
        del model[start:stop:step]
        del lst[start:stop:step]
    assert list(model) == lst


def test_clear() -> None:
    model = RQList([8, 4, 5])
    model.clear()

    assert len(list(model)) == 0


def test_insert() -> None:
    model = RQList([5])
    connect_signal(model.rq_data_changed)
    connect_int_signal(model.rq_list_insert)

    model.insert(index=1, item=7)
    assert_signal_emitted(model.rq_data_changed)
    assert_int_signal(model.rq_list_insert, 1)
    assert list(model) == [5, 7]

    model.insert(index=0, item=3)
    assert_signal_emitted(model.rq_data_changed)
    assert_int_signal(model.rq_list_insert, 0)
    assert list(model) == [3, 5, 7]


def test_append() -> None:
    model = RQList([7])
    connect_signal(model.rq_data_changed)
    connect_int_signal(model.rq_list_insert)

    model.append(3)
    assert_signal_emitted(model.rq_data_changed)
    assert_int_signal(model.rq_list_insert, 1)
    assert list(model) == [7, 3]


def test_set() -> None:
    model = RQList([7, 4, 6])
    model.set([1, 4, 8])

    assert list(model) == [1, 4, 8]


def test_get() -> None:
    model = RQList([7, 4, 6])
    assert model.get() == [7, 4, 6]


def test_remove() -> None:
    model = RQList([2, 7, 43, 2, 67])
    model.remove(2)

    assert list(model) == [7, 43, 2, 67]


def test_remove_all() -> None:
    model = RQList([2, 7, 43, 2, 67])
    model.remove_all(2)

    assert list(model) == [7, 43, 67]


def test_get_item() -> None:
    model = RQList([2, 7, 43, 2, 67])

    assert model[0] == 2
    assert model[2] == 43


def test_index() -> None:
    model = RQList([2, 7, 43, 2, 67])

    assert model.index(2) == 0
    assert model.index(7) == 1


def test_iteration() -> None:
    model = RQList([1, 2, 3])

    for i in model:
        assert i in range(1, 4)


def test_length() -> None:
    model = RQList([2, 7, 43, 2, 67])

    assert len(model) == 5


def test_count() -> None:
    model = RQList([2, 7, 43, 2, 67, 2])

    assert model.count(2) == 3


def test_extend() -> None:
    model = RQList([2, 7])

    model.extend([6, 34])
    assert list(model) == [2, 7, 6, 34]


def test_contains() -> None:
    model = RQList([2, 7])
    assert 7 in model


def test_rq_models_deletion() -> None:
    model1 = RQModel()

    class SubModel(RQModel):

        def set(self, value: Any) -> None:
            raise NotImplementedError

        def get(self) -> Any:
            raise NotImplementedError

    model2 = SubModel()

    model = RQList([model1])
    assert len(model) == 1
    model.append(model2)
    assert len(model) == 2
    model1.__del__()  # pylint: disable=unnecessary-dunder-call
    assert len(model) == 1
    model2.__del__()  # pylint: disable=unnecessary-dunder-call
    assert len(model) == 0


def test_reactive_indexes() -> None:
    class Class:
        pass

    class_a = Class()
    class_b = Class()
    class_c = Class()
    model = RQList([class_a, class_b])
    a_index = model.reactive_index(class_a)
    b_index = model.reactive_index(class_b)
    assert a_index.get() == 0
    assert b_index.get() == 1
    model.append(class_c)
    c_index = model.reactive_index(class_c)

    assert c_index.get() == 2

    model.remove(class_a)
    assert b_index.get() == 0
    assert c_index.get() == 1


def test_computed() -> None:
    numbers = RQList([1, 6, 3, 34, 77, 5, 82])
    threshold = RQInt(0)

    greater_numbers = RQComputedList(
        function=lambda numbers, threshold: [number for number in numbers if number > threshold],
        numbers=numbers,
        threshold=threshold
    )

    assert list(greater_numbers) == [1, 6, 3, 34, 77, 5, 82]
    threshold.set(7)
    assert list(greater_numbers) == [34, 77, 82]
    threshold.set(55)
    assert list(greater_numbers) == [77, 82]
    numbers.remove(77)
    assert list(greater_numbers) == [82]
    assert greater_numbers.get() == [82]
