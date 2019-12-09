from dataclasses import dataclass, InitVar, field
import pandas as pd

DF = pd.DataFrame


class StructureError(Exception):
    pass


@dataclass
class Structure:
    candidates_df: InitVar[DF]  # assumes candidates_df nodes are *IN STRUCTURAL ORDER*
    nodes_df: InitVar[DF]
    elements_df: InitVar[DF]
    extents_df: InitVar[DF]
    df: DF = field(init=False)

    def __post_init__(self, candidates_df: DF, nodes_df: DF, elements_df: DF, extents_df: DF):
        self.df = _struct_df(candidates_df, nodes_df, extents_df)


def _struct_df(candidates_df: DF, nodes_df: DF, extents_df: DF) -> pd.DataFrame:
    # remove extents nodes from candidates
    candidates_df = candidates_df.loc[~candidates_df["n"].isin(extents_df["n"]), :]
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
