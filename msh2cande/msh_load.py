from pathlib import Path
from typing import Sequence, NamedTuple
import pandas as pd


class Msh(NamedTuple):
    nodes: pd.DataFrame = None
    elements: pd.DataFrame = None
    boundaries: pd.DataFrame = None

    @classmethod
    def load_msh(cls, path: Path):
        return _load_msh(path)


def _main(msh_path: Path, materials=None, steps=None) -> None:
    msh = Msh.load_msh(msh_path)


def _n_nodes(msh_lines_df: pd.DataFrame) -> int:
    n = msh_lines_df.iloc[0,0]
    msh_lines_df.drop(index=0, inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return int(n)


def _nodes(msh_lines_df: pd.DataFrame, n_nodes: int) -> pd.DataFrame:
    nodes_df: pd.DataFrame = msh_lines_df.iloc[:n_nodes, 0].str.strip().str.split(expand=True)
    nodes_df.columns = list("nxy")
    nodes_df.set_index("n", inplace=True)
    msh_lines_df.drop(index=range(n_nodes), inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return nodes_df


def _n_elements(msh_lines_df: pd.DataFrame) -> int:
    n = msh_lines_df.iloc[0,0]
    msh_lines_df.drop(index=0, inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return int(n)


def _elements(msh_lines_df: pd.DataFrame, n_elements: int) -> pd.DataFrame:
    elements_df: pd.DataFrame = msh_lines_df.iloc[:n_elements, 0].str.strip().str.split(expand=True)
    elements_df.columns = list("nijkl")
    elements_df.set_index("n", inplace=True)
    msh_lines_df.drop(index=range(n_elements), inplace=True)
    msh_lines_df.reset_index(inplace=True, drop=True)
    return elements_df


def _boundaries(msh_lines: pd.DataFrame) -> pd.DataFrame:
    return NotImplemented


def _load_msh_df(msh_str: Sequence[str]) -> pd.DataFrame:
    return pd.DataFrame(msh_str, columns=["lines"])


def _load_msh_seq(msh_str: Sequence[str]) -> Msh:
    msh_lines_df = _load_msh_df(msh_str)
    n_nodes: int = _n_nodes(msh_lines_df)
    nodes: pd.DataFrame = _nodes(msh_lines_df, n_nodes)
    n_elements: int = _n_elements(msh_lines_df)
    elements: pd.DataFrame = _elements(msh_lines_df, n_elements)
    boundaries: pd.DataFrame = _boundaries(msh_lines_df)
    return Msh(nodes, elements, boundaries)


def _load_msh(msh_path: Path) -> Msh:
    with msh_path.open() as f:
        return _load_msh_seq(f.readlines())
