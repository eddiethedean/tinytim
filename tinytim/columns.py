from typing import Dict, Generator, MutableMapping, MutableSequence, Tuple

from tinytim.features import column_names


def column_dict(data, col: str) -> Dict[str, MutableSequence]:
    return {col: data[col]}


def itercolumns(data: MutableMapping) -> Generator[Tuple[str, tuple], None, None]:
    """Return a generator of tuple column name, column values."""
    for col in column_names(data):
        yield col, tuple(data[col])