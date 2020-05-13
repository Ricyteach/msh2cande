import pytest

from msh2cande.seqview import SeqItemView, DelegatedInteger, SeqNumberView
import pandas as pd


@pytest.fixture
def delegated_integer_class():
    class C(DelegatedInteger):
        v = 1
        @property
        def value(self):
            return self.v
    return C


@pytest.fixture
def delegated_obj(delegated_integer_class):
    return delegated_integer_class()


def test_delegated_integer_obj(delegated_obj):
    assert delegated_obj
    assert delegated_obj + 1 == 2
    assert delegated_obj - 1 == 0
    assert delegated_obj * 5 == 5
    assert delegated_obj / 2 == 0.5
    assert delegated_obj // 2 == 0
    assert delegated_obj ** 0.5 == 1.0
    assert -delegated_obj == -1
    assert +-delegated_obj == -1
    assert abs(+-delegated_obj) == 1
    assert delegated_obj % 2 == 1
    assert delegated_obj % 1 == 0


@pytest.fixture
def dataframe():
    return pd.DataFrame(index=[1,2,3,4,5,6], columns=list('a'))


@pytest.fixture
def seq(dataframe):
    return dataframe.index.values


@pytest.fixture
def key():
    return 3


@pytest.fixture
def seq_item_view_obj(seq, key):
    return SeqItemView(key, seq)


def test_seq_item_view_obj(seq_item_view_obj, seq, key):
    assert seq_item_view_obj.value == seq[key]
    assert seq_item_view_obj == seq[key]
    assert repr(seq_item_view_obj) == f"SeqItemView({seq!r}, {key!r})"
    assert str(seq_item_view_obj) == f"{seq[key]!s}"
    assert not bool(seq_item_view_obj) == False


@pytest.fixture
def seq_number_view_obj(seq, key):
    return SeqNumberView(key, seq)


import operator as op


@pytest.mark.parametrize("ifunc, func",
                         [
                             (op.iadd, op.add),
                             (op.isub, op.sub),
                             (op.imul, op.mul),
                             (op.itruediv, op.truediv),
                             (op.ifloordiv, op.floordiv),
                             (op.imod, op.mod),
                             (op.ipow, op.pow),
                         ])
def test_seq_number_view_obj_operators(ifunc, func, seq_number_view_obj, seq, key, dataframe):
    original = dataframe.index[key]
    ifunc(seq_number_view_obj, 1)
    assert dataframe.index[key] == func(original, 1)
