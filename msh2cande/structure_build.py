from dataclasses import dataclass, InitVar, field
from typing import Optional
import pandas as pd
import plotly.graph_objects as go

from msh2cande.common import _nodes_by_number

DF = pd.DataFrame


class StructureError(Exception):
    pass


@dataclass
class Structure:
    candidates_df: DF  # assumes df nodes are *IN STRUCTURAL ORDER*
    nodes_df: InitVar[DF]
    elements_df: InitVar[DF]
    extents_df: InitVar[DF]
    df: DF = field(init=False)

    def __post_init__(self, nodes_df: DF, elements_df: DF, extents_df: DF):
        self.df = _struct_df(self.candidates_df, nodes_df, extents_df)
        self.candidates_df = _nodes_by_number(self.candidates_df, seq=self.df["n"])
        self.candidates_df = self.candidates_df.reset_index(drop=True)
        self.candidates_df.index += 1
        self.candidates_df["x"] = nodes_df.loc[self.candidates_df["n"], "x"].values
        self.candidates_df["y"] = nodes_df.loc[self.candidates_df["n"], "y"].values

    def show_candidates(self):
        _show_nodes_df(self.candidates_df)

    def remove_candidates(self, *args, seq = None):
        self.candidates_df = _nodes_by_number(self.candidates_df, *args, seq=seq, remove=True)

    def keep_candidates(self, *args, seq = None):
        self.candidates_df = _nodes_by_number(self.candidates_df, *args, seq=seq, remove=False)


def _struct_df(candidates_df: DF, nodes_df: DF, extents_df: Optional[DF] = None) -> DF:
    if extents_df is not None:
        # remove extents nodes from candidates
        candidates_df = _nodes_by_number(candidates_df, seq=extents_df["n"], remove=True)
    return _updated_struct_df_from_candidates(candidates_df, nodes_df)


def _updated_struct_df_from_candidates(candidates_df: DF, nodes_df: DF) -> DF:
    # build structure dataframe
    struct_df = pd.DataFrame(
        index=pd.MultiIndex.from_product([range(1, len(candidates_df)), list("ij")], names=["e", "ij"]),
        columns=list("nxy")
    )
    inodes = nodes_df.loc[candidates_df.iloc[1:, 0], :]
    jnodes = nodes_df.loc[candidates_df.iloc[:-1, 0], :]
    struct_df.loc[(slice(None), "i"), :] = inodes.reset_index().values
    struct_df.loc[(slice(None), "j"), :] = jnodes.reset_index().values
    return struct_df


def _show_nodes_df(df: DF) -> None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = df.x, y = df.y,
        name='candidate nodes',
        marker_color='rgba(152, 0, 0, .8)',
        text=df.index,
        textposition="top center",
    ))

    # Set options common to all traces with fig.update_traces
    fig.update_traces(mode='markers+text', marker_line_width=2, marker_size=10)
    fig.update_layout(title='Styled Scatter',
                      yaxis_zeroline=False, xaxis_zeroline=False)
    fig.show()
