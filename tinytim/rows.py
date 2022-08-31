from typing import Generator, Mapping, MutableMapping, Tuple

import tinytim.data as data_features


def row_dict(data: Mapping, index: int) -> dict: 
    """Return one row from data at index."""
    return {col: data_features.table_value(data, col, index) for col in data_features.column_names(data)}


def row_values(data: MutableMapping, index: int) -> tuple:
    """Return a tuple of the values at row index."""
    return tuple(values[index] for values in data.values())


def iterrows(data: Mapping) -> Generator[Tuple[int, dict], None, None]:
    """Return a generator of tuple row index, row dict values."""
    for i in data_features.index(data):
        yield i, row_dict(data, i)


def itertuples(data: MutableMapping) -> Generator[tuple, None, None]:
    """Return a generator of tuple row values."""
    for _, row in iterrows(data):
        yield tuple(row.values())


def itervalues(data: MutableMapping) -> Generator[tuple, None, None]:
    """Return a generator of tuple row values."""
    for i, row in iterrows(data):
        yield tuple(row.values())


def values(data: MutableMapping) -> Tuple[tuple]:
    """Return tuple of tuple row values."""
    return tuple(itervalues(data))