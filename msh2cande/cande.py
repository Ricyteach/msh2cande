from enum import Enum
from functools import partial
import pandas as pd
from msh2cande import format as fmt


class L3(Enum):
    c2 = partial(fmt.c2)
    c3 = partial(fmt.c3)
    c4 = partial(fmt.c4)
    c5 = partial(fmt.c5)

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def format_df(self, df):
        return _L3_format(df, self)


def _L3_format(df: pd.DataFrame, l3_fmt: L3):
    df_reset = df.reset_index() if l3_fmt is not L3.c5 else df
    return df_reset.apply(lambda srs: l3_fmt(**srs), axis=1)
