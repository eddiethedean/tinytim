from typing import Dict, Generator, MutableMapping, MutableSequence, Tuple

import tinytim.data as data_features


def column_dict(data, col: str) -> Dict[str, MutableSequence]:
    return {col: data[col]}


def itercolumns(data: MutableMapping) -> Generator[Tuple[str, tuple], None, None]:
    """Return a generator of tuple column name, column values."""
    for col in data_features.column_names(data):
        yield col, tuple(data[col])