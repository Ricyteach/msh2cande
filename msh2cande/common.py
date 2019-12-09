import operator as op


def _nodes_by_number(df, *args, seq = None, remove=False):
    """Filter out nodes from a node dataframe by node number.

    Provide a node number, a number range, or a sequence/series of numbers.

    Specify remove=True to remove instead of get. Assumes nodes are stored at column "n"."""
    maybe_invert = {True: op.invert, False: lambda x: x}[remove]
    seq_arg = len(seq) if seq is not None else None
    if seq_arg and args:
        raise ValueError("only a sequence of nodes or specified node numbers can be removed, not both")
    if seq_arg:
        get_isin_arg = lambda: seq
    else:
        try:
            get_isin_arg = {0: lambda: [], 1: lambda: [args[0]]}.get(len(args), lambda: range(*args))
        except TypeError:
            raise ValueError("maximum 3 additional positional arguments allowed")
    isin_arg = get_isin_arg()
    node_filter = maybe_invert(df["n"].isin(isin_arg))
    return df.loc[df.index[node_filter], :]
