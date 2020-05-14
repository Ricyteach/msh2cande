import itertools
from pathlib import Path
from typing import Sequence, NamedTuple, Callable
import pandas as pd

from msh2cande.seqview import SeqNumberView

DF = pd.DataFrame


class Msh(NamedTuple):
    nodes: DF = None
    elements: DF = None
    boundaries: DF = None

    @classmethod
    def load_msh(cls, path: Path, *, clean: bool = True):
        loaded_msh = _load_msh(path)
        if clean:
            _clean_msh(loaded_msh)
        return loaded_msh


def _n_nodes(msh_lines_df: DF) -> int:
    n = msh_lines_df.iloc[0,0]
    msh_lines_df.drop(index=0, inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return int(n)


def _nodes(msh_lines_df: DF, n_nodes: int) -> DF:
    nodes_df: DF = msh_lines_df.iloc[:n_nodes, 0].str.strip().str.split(expand=True)
    nodes_df.columns = list("nxy")
    nodes_df["n"] = nodes_df["n"].apply(int)
    nodes_df.set_index("n", inplace=True)
    nodes_df = nodes_df.applymap(float)
    msh_lines_df.drop(index=range(n_nodes), inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return nodes_df


def _n_elements(msh_lines_df: DF) -> int:
    n = msh_lines_df.iloc[0,0]
    msh_lines_df.drop(index=0, inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return int(n)


def _elements(msh_lines_df: DF, n_elements: int, nodes: DF) -> DF:
    elements_df: DF = msh_lines_df.iloc[:n_elements, 0].str.strip().str.split(expand=True)
    elements_df.columns = list("eijkl")
    elements_df = elements_df.applymap(int)
    elements_df.set_index("e", inplace=True)
    elements_df = elements_df.applymap(nodes_numbers_view_factory(nodes))
    msh_lines_df.drop(index=range(n_elements), inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return elements_df


def _boundaries(msh_lines: DF, nodes: DF) -> DF:
    boundaries_df = msh_lines.iloc[:, 0].str.strip().str.split(expand=True)
    boundaries_df.columns = list("bn")
    boundaries_df = boundaries_df[~boundaries_df["n"].isnull()]
    boundaries_df = boundaries_df.applymap(int)
    boundaries_df.drop(columns="b", inplace=True)
    boundaries_df.index.name = "b"
    boundaries_df.reset_index(inplace=True, drop=True)
    boundaries_df.index+=1
    boundaries_df = boundaries_df.applymap(nodes_numbers_view_factory(nodes))
    return boundaries_df


def _load_msh_df(msh_str: Sequence[str]) -> DF:
    return DF(msh_str, columns=["lines"])


def _load_msh_seq(msh_str: Sequence[str]) -> Msh:
    msh_lines_df = _load_msh_df(msh_str)
    n_nodes: int = _n_nodes(msh_lines_df)
    nodes: DF = _nodes(msh_lines_df, n_nodes)
    n_elements: int = _n_elements(msh_lines_df)
    elements: DF = _elements(msh_lines_df, n_elements, nodes)
    boundaries: DF = _boundaries(msh_lines_df, nodes)
    return Msh(nodes, elements, boundaries)


def _load_msh(msh_path: Path) -> Msh:
    with msh_path.open() as f:
        return _load_msh_seq(f.readlines())


def _extents(nodes_df: DF, boundaries_df: DF):
    boundaries_xy_df = nodes_df.loc[boundaries_df['n'], :]
    minx = boundaries_xy_df['x'].min()
    maxx = boundaries_xy_df['x'].max()
    miny = boundaries_xy_df['y'].min()
    maxy = boundaries_xy_df['y'].max()
    at_extents = (boundaries_xy_df['x']==minx) | (boundaries_xy_df['x']==maxx) | (boundaries_xy_df['y']==miny) | (boundaries_xy_df['y']==maxy)
    extents_df = boundaries_df.loc[boundaries_df.index[at_extents], :]
    extents_xy_df = nodes_df.loc[extents_df['n'], :]
    extents_df['xcode'] = ((extents_xy_df['x'] == minx) | (extents_xy_df['x'] == maxx)).astype(int).values
    extents_df['xvalue'] = 0
    extents_df['ycode'] = (extents_xy_df['y'] == miny).astype(int).values
    extents_df['yvalue'] = 0
    extents_df['angle'] = 0
    # get all extents nodes excluding any top of mesh nodes that are x-free
    step1 = (extents_xy_df['y'] != maxy).values | (extents_df['xcode'] != 0)
    extents_df['step'] = step1.astype(int).values
    extents_df = extents_df.reset_index(drop=True)
    extents_df.index += 1
    return extents_df


def nodes_numbers_view_factory(nodes: DF) -> Callable[[int], SeqNumberView]:
    nodes_index = nodes.index

    def f(key: int):
        index = nodes_index.get_loc(key)
        return SeqNumberView(index, nodes_index.values)
    return f


def _clean_msh(msh: Msh):
    """Fix common problems with Msh objects newly loaded from .msh file."""
    _dedup_nodes(msh)


def _dedup_nodes(msh: Msh, tol=0.001):
    """Modify Msh object such that all nodes are assumed to be unique."""

    nodes_df = msh.nodes

    # change node numbering of firsts (including nodes that later have a dup)
    c = itertools.count(start=1)
    firsts_slicer = (nodes_df.duplicated() ^ nodes_df.duplicated(keep=False)) | ~ nodes_df.duplicated(keep=False)
    firsts_index = nodes_df[firsts_slicer].index
    # temporarily convert first indexes to strs so not overwritten later
    nodes_df.rename({index:str(next(c)) for index in firsts_index}, inplace=True)

    # get first duplicated nodes ("duped", excluding the duplicates that come after)
    duped_slicer = nodes_df.duplicated() ^ nodes_df.duplicated(keep=False)
    duped_index = nodes_df.index[duped_slicer]

    # change the duplicate node numbers to match the first dupe
    for duped_node_index in duped_index:
        dupes_w_first_slicer = (nodes_df == nodes_df.loc[duped_node_index]).all(axis=1)
        dupes_w_first_index = nodes_df[dupes_w_first_slicer].index
        nodes_df.rename({index:duped_node_index for index in dupes_w_first_index if not isinstance(index, str)}, inplace=True)

    # change nodes index back to ints; must use nodes_df.rename(inplace=True) to maintain element and boundary
    # references to underlying index; yes this is probably slow
    nodes_df.rename({index_str: int(index_str) for index_str in nodes_df.index}, inplace=True)

    # TODO: clean duplicate boundaries

    # # dupes (excluding any firsts)
    # dupes_slicer = nodes_df.duplicated()
    # dupes_index = nodes_df.index[dupes_slicer]
    #
