from pathlib import Path

from msh2cande.msh_load import Msh


def _main(msh_path: Path, materials=None, steps=None) -> None:
    msh = Msh.load_msh(msh_path)
