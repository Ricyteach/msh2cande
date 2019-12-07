import pytest

from msh2cande.msh_load import _load_msh_df, _n_nodes, _nodes, _n_elements, _elements, _boundaries


##
# NOTE: the INCLUSION and also the ORDER of fixtures in signatures matters!
##

@pytest.fixture(scope="module")
def msh_lines_df(MSH_STR):
    return _load_msh_df(MSH_STR.split("\n"))


@pytest.fixture(scope="module")
def len_msh_lines(msh_lines_df):
    return len(msh_lines_df)


@pytest.fixture(scope="module")
def n_nodes(msh_lines_df, len_msh_lines):
    return _n_nodes(msh_lines_df)


@pytest.fixture(scope="module")
def nodes_df(msh_lines_df, len_msh_lines, n_nodes):
    return _nodes(msh_lines_df, n_nodes)


@pytest.fixture(scope="module")
def n_elements(msh_lines_df, len_msh_lines, n_nodes, nodes_df):
    return _n_elements(msh_lines_df)


@pytest.fixture(scope="module")
def elements_df(msh_lines_df, len_msh_lines, n_nodes, nodes_df, n_elements):
    return _elements(msh_lines_df, n_elements)


@pytest.fixture(scope="module")
def boundaries_df(msh_lines_df, len_msh_lines, n_nodes, nodes_df, n_elements, elements_df):
    return _boundaries(msh_lines_df)
