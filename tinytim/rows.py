from collections import defaultdict
from typing import Dict, Generator, Mapping, MutableMapping, Sequence, Tuple

import tinytim.data as data_features


def row_dict(
    data: Mapping,
    index: int
) -> dict: 
    """
    Return one row from data at index.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    index : int
        row index

    Returns
    -------
    dict
        one row from data at index

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> row_dict(data, 1)
    {'x': 2, 'y': 7}
    """
    return {col: data_features.table_value(data, col, index)
                for col in data_features.column_names(data)}


def row_values(
    data: MutableMapping,
    index: int
) -> tuple:
    """
    Return a tuple of the values at row index.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    index : int
        row index

    Returns
    -------
    tuple
        values at row index

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> row_values(data, 0)
    (1, 6)
    """
    return tuple(values[index] for values in data.values())


def iterrows(
    data: Mapping
) -> Generator[Tuple[int, dict], None, None]:
    """
    Return a generator of tuple row index, row dict values.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}

    Returns
    -------
    generator[tuple[int, dict]]
        generator of tuple (row index, row dict values)

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> generator = iterrows(data)
    >>> next(generator)
    (0, {'x': 1, 'y': 6})
    >>> next(generator)
    (1, {'x': 2, 'y': 7})
    >>> next(generator)
    (2, {'x': 3, 'y': 8})
    >>> next(generator)
    ...
    StopIteration
    """
    for i in data_features.index(data):
        yield i, row_dict(data, i)


def itertuples(
    data: Mapping
) -> Generator[tuple, None, None]:
    """
    Return a generator of tuple row values.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}

    Returns
    -------
    generator[tuple]
        generator of tuple row values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> generator = iterrows(data)
    >>> next(generator)
    (1, 6)
    >>> next(generator)
    (2, 7)
    >>> next(generator)
    (3, 8)
    >>> next(generator)
    ...
    StopIteration
    """
    for _, row in iterrows(data):
        yield tuple(row.values())


def itervalues(
    data: MutableMapping
) -> Generator[tuple, None, None]:
    """
    Return a generator of tuple row values.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}

    Returns
    -------
    generator[tuple]
        generator of tuple row values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> generator = itervalues(data)
    >>> next(generator)
    (1, 6)
    >>> next(generator)
    (2, 7)
    >>> next(generator)
    (3, 8)
    >>> next(generator)
    ...
    StopIteration
    """
    return itertuples(data)


def values(
    data: MutableMapping
) -> Tuple[tuple]:
    """
    Return tuple of tuple row values.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}

    Returns
    -------
    tuple[tuple]
        tuple of tuple row values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> values(data)
    ((1, 6), (2, 7), (3, 8))
    """
    return tuple(itervalues(data))


def row_value_counts(
    data: Mapping[str, Sequence],
    sort=True,
    ascending=True
) -> Dict[tuple, int]:
    """
    Count up the unique rows.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    sort : bool, optional
        sort the results by count
    ascending : bool, optional
        if sort=True, sort highest to lowest

    Returns
    -------
    dict[tuple, int]
        {(row values), count}

    Example
    -------
    >>> data = {'x': [1, 2, 3, 3], 'y': [6, 7, 3, 3]}
    >>> row_value_counts(data)
    {(3, 3): 2, (1, 6): 1, (2, 7): 1}
    """
    d = defaultdict(int)
    for row in itertuples(data):
        d[row] += 1
    if sort:
        return dict(sorted(d.items(),
                           key=lambda item: item[1],
                           reverse=ascending))
    else:
        return dict(d)