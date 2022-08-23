from typing import Generator, MutableMapping, Tuple

from tinytim.features import column_names, index, table_value


def row_dict(data: MutableMapping, index: int) -> dict: 
    """Return one row from data at index."""
    return {col: table_value(data, col, index) for col in column_names(data)}


def row_values(data: MutableMapping, index: int) -> tuple:
    """Return a tuple of the values at row index."""
    return tuple(values[index] for values in data.values())


def iterrows(data: MutableMapping) -> Generator[Tuple[int, dict], None, None]:
    """Return a generator of tuple row index, row dict values."""
    for i in index(data):
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