from pathlib import Path
from typing import Sequence, NamedTuple
import pandas as pd

DF = pd.DataFrame


class Msh(NamedTuple):
    nodes: DF = None
    elements: DF = None
    boundaries: DF = None

    @classmethod
    def load_msh(cls, path: Path):
        return _load_msh(path)


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


def _elements(msh_lines_df: DF, n_elements: int) -> DF:
    elements_df: DF = msh_lines_df.iloc[:n_elements, 0].str.strip().str.split(expand=True)
    elements_df.columns = list("eijkl")
    elements_df = elements_df.applymap(int)
    elements_df.set_index("e", inplace=True)
    msh_lines_df.drop(index=range(n_elements), inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return elements_df


def _boundaries(msh_lines: DF) -> DF:
    boundaries_df = msh_lines.iloc[:, 0].str.strip().str.split(expand=True)
    boundaries_df.columns = list("bn")
    boundaries_df = boundaries_df[~boundaries_df["n"].isnull()]
    boundaries_df = boundaries_df.applymap(int)
    boundaries_df.drop(columns="b", inplace=True)
    boundaries_df.index.name = "b"
    boundaries_df.reset_index(inplace=True, drop=True)
    boundaries_df.index+=1
    return boundaries_df


def _load_msh_df(msh_str: Sequence[str]) -> DF:
    return DF(msh_str, columns=["lines"])


def _load_msh_seq(msh_str: Sequence[str]) -> Msh:
    msh_lines_df = _load_msh_df(msh_str)
    n_nodes: int = _n_nodes(msh_lines_df)
    nodes: DF = _nodes(msh_lines_df, n_nodes)
    n_elements: int = _n_elements(msh_lines_df)
    elements: DF = _elements(msh_lines_df, n_elements)
    boundaries: DF = _boundaries(msh_lines_df)
    return Msh(nodes, elements, boundaries)


def _load_msh(msh_path: Path) -> Msh:
    with msh_path.open() as f:
        return _load_msh_seq(f.readlines())
