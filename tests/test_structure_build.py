import pytest
from msh2cande.structure_build import _struct_df, Structure


@pytest.fixture(scope="module")
def struct_df_dirty(boundaries_df, nodes_df, elements_df, extents_df):
    return _struct_df(boundaries_df, nodes_df, extents_df)


@pytest.fixture(scope="module")
def structure(boundaries_df, nodes_df, elements_df, extents_df):
    return  Structure(boundaries_df, nodes_df, elements_df, extents_df)


def test_struct_df(struct_df_dirty, N_EXTENTS, N_BOUNDARIES):
    assert len(struct_df_dirty) == 2 * (N_BOUNDARIES - N_EXTENTS - 1)


def test_struct(structure):
    assert structure


def test_structure_show_candidates(structure):
    structure.show_candidates()
