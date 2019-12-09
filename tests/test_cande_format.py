import pytest
from msh2cande.cande import L3


@pytest.fixture(scope="module")
def elements_df(elements_df):
    elements_df['mat'] = 0
    elements_df['step'] = 0
    return elements_df


def test_format_c3(nodes_df, N_NODES):
    cande_str = L3.c3.format_df(nodes_df)
    assert len(cande_str) == N_NODES


def test_format_c4(elements_df, N_ELEMENTS):
    cande_str = L3.c4.format_df(elements_df)
    assert len(cande_str) == N_ELEMENTS


def test_format_c5(boundaries_df, N_BOUNDARIES):
    cande_str = L3.c5.format_df(boundaries_df)
    assert len(cande_str) == N_BOUNDARIES
