from pyreaqtive import RQList, RQModel
from .signal_checker import *


def test_init():
    initial = [1, 6, 4]
    m = RQList(initial_items=initial)

    assert m._list == initial

    m = RQList()
    assert m._list == []


def test_del():
    m = RQList([8, 4, 5])

    connect_signal(m.rq_data_changed)
    connect_int_signal(m.rq_list_remove)
    del m[1]
    assert_int_signal(m.rq_list_remove, 1)
    assert list(m) == [8, 5]

    m.pop()
    assert_signal_emitted(m.rq_data_changed)
    assert_int_signal(m.rq_list_remove, 1)
    assert list(m) == [8]
    m.pop()
    assert_signal_emitted(m.rq_data_changed)
    assert_int_signal(m.rq_list_remove, 0)
    assert list(m) == []


def test_clear():
    m = RQList([8, 4, 5])
    m.clear()

    assert list(m) == []


def test_insert():
    m = RQList([5])
    connect_signal(m.rq_data_changed)
    connect_int_signal(m.rq_list_insert)

    m.insert(index=1, item=7)
    assert_signal_emitted(m.rq_data_changed)
    assert_int_signal(m.rq_list_insert, 1)
    assert list(m) == [5, 7]

    m.insert(index=0, item=3)
    assert_signal_emitted(m.rq_data_changed)
    assert_int_signal(m.rq_list_insert, 0)
    assert list(m) == [3, 5, 7]


def test_append():
    m = RQList([7])
    connect_signal(m.rq_data_changed)
    connect_int_signal(m.rq_list_insert)

    m.append(3)
    assert_signal_emitted(m.rq_data_changed)
    assert_int_signal(m.rq_list_insert, 1)
    assert list(m) == [7, 3]


def test_set():
    m = RQList([7, 4, 6])
    m.set([1, 4, 8])

    assert list(m) == [1, 4, 8]


def test_get():
    m = RQList([7, 4, 6])
    assert m.get() == [7, 4, 6]


def test_remove():
    m = RQList([2, 7, 43, 2, 67])
    m.remove(2)

    assert list(m) == [7, 43, 2, 67]


def test_remove_all():
    m = RQList([2, 7, 43, 2, 67])
    m.remove_all(2)

    assert list(m) == [7, 43, 67]


def test_get_item():
    m = RQList([2, 7, 43, 2, 67])

    assert m[0] == 2
    assert m[2] == 43


def test_index():
    m = RQList([2, 7, 43, 2, 67])

    assert m.index(2) == 0
    assert m.index(7) == 1


def test_reactive_indexes():
    # TODO
    pass


def test_iteration():
    m = RQList([1, 2, 3])

    for i in m:
        assert i in range(1, 4)


def test_length():
    m = RQList([2, 7, 43, 2, 67])

    assert len(m) == 5


def test_count():
    m = RQList([2, 7, 43, 2, 67, 2])

    assert m.count(2) == 3


def test_extend():
    m = RQList([2, 7])

    m.extend([6, 34])
    assert list(m) == [2, 7, 6, 34]


def test_contains():
    m = RQList([2, 7])
    assert 7 in m


def test_rq_models_deletion():
    m1 = RQModel()

    class SubModel(RQModel):
        pass

    m2 = SubModel()

    m = RQList([m1])
    assert len(m) == 1
    m.append(m2)
    assert len(m) == 2
    m1.__delete__()
    assert len(m) == 1
    m2.__delete__()
    assert len(m) == 0


def test_reactive_indexes():
    class Class:
        pass

    a = Class()
    b = Class()
    c = Class()
    m = RQList([a, b])
    ai = m.reactive_index(a)
    bi = m.reactive_index(b)
    assert ai.get() == 0
    assert bi.get() == 1
    m.append(c)
    ci = m.reactive_index(c)

    assert ci.get() == 2

    m.remove(a)
    assert bi.get() == 0
    assert ci.get() == 1


def test_computed():
    pass
