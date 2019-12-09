import numpy as np


def test_n_nodes(len_msh_lines, msh_lines_df, n_nodes, N_NODES):
    assert n_nodes==N_NODES
    assert len_msh_lines == len(msh_lines_df)+1
    assert msh_lines_df.index[0]==0


def test_nodes(len_msh_lines, msh_lines_df, n_nodes, nodes_df):
    assert nodes_df.x.dtype==np.dtype(float)
    assert nodes_df.y.dtype==np.dtype(float)
    assert len(nodes_df) == n_nodes
    assert len_msh_lines == len(msh_lines_df)+1+n_nodes
    assert msh_lines_df.index[0]==0


def test_n_elements(len_msh_lines, msh_lines_df, n_nodes, n_elements, N_ELEMENTS):
    assert n_elements==N_ELEMENTS
    assert len_msh_lines == len(msh_lines_df)+1+n_nodes+1
    assert msh_lines_df.index[0]==0


def test_elements(len_msh_lines, msh_lines_df, n_nodes, n_elements, elements_df):
    assert len(elements_df) == n_elements
    assert len_msh_lines == len(msh_lines_df)+1+n_nodes+1+n_elements
    assert msh_lines_df.index[0]==0


def test_boundaries(boundaries_df, N_BOUNDARIES):
    assert len(boundaries_df) == N_BOUNDARIES


def test_extents(extents_df, N_EXTENTS):
    assert len(extents_df) == N_EXTENTS
