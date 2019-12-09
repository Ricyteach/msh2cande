import pytest
from msh2cande.structure_build import _struct_df


@pytest.fixture(scope="module")
def struct_df_dirty(boundaries_df, nodes_df, elements_df, extents_df):
    return _struct_df(boundaries_df, nodes_df, extents_df)


def test_struct_df(struct_df_dirty, N_EXTENTS, N_BOUNDARIES):
    assert len(struct_df_dirty) == 2 * (N_BOUNDARIES - N_EXTENTS - 1)
