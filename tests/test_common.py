import pytest
from msh2cande.common import _nodes_by_number
import pandas as pd


@pytest.fixture(scope="function")
def nodes_df(nodes_df):
    return nodes_df


def test_nodes_by_number_single(nodes_df):
    assert len(_nodes_by_number(nodes_df.reset_index(), 1)) == 1


@pytest.mark.parametrize("rng_args, result", [
    [(1,2), 1],
    [(1,3), 2],
    [(1,4,2), 2],
], ids=["one", "two", "step=2"])
def test_nodes_by_number_range(rng_args, result, nodes_df):
    assert len(_nodes_by_number(nodes_df.reset_index(), *rng_args)) == result


def test_nodes_by_number_single_remove(nodes_df, N_NODES):
    assert len(_nodes_by_number(nodes_df.reset_index(), 1, remove=True)) == N_NODES-1


@pytest.mark.parametrize("rng_args", [
    (1, 2),
    (1,3),
    (1,4,2),
], ids=["one", "two", "step=2"])
def test_nodes_by_number_range_remove(rng_args: range, nodes_df, N_NODES):
    assert len(_nodes_by_number(nodes_df.reset_index(), *rng_args, remove=True)) == N_NODES-len(range(*rng_args))


def test_nodes_by_number_seq(nodes_df):
    assert len(_nodes_by_number(nodes_df.reset_index(), seq=pd.Series([1]).values)) == 1


def test_nodes_by_number_seq_remove(nodes_df, N_NODES):
    assert len(_nodes_by_number(nodes_df.reset_index(), seq=pd.Series([1]).values, remove=True)) == N_NODES-1
