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


def records(d: Mapping[str, Sequence]) -> Generator[Mapping, None, None]:
    """
    Yield each record (row) in d.
    
    Parameters
    ----------
    d : Mapping[str, Sequence]
        data mapping of {column name: column values}
    
    Example
    -------
    >>> d = {'x': [1, 2, 3, 4], 'y': [55, 66, 77, 88]}
    >>> generator = records(d)
    >>> next(generator)
    {'x': 1, 'y': 55}
    >>> next(generator)
    {'x': 2, 'y': 66}
    >>> next(generator)
    {'x': 3, 'y': 77}
    >>> next(generator)
    {'x': 4, 'y': 88}
    """
    for _, record in iterrows(d):
        yield record
    

def records_equal(d1: Mapping[str, Sequence], d2: Mapping[str, Sequence]) -> bool:
    """
    Compare d1 and d2 records (rows) to see if they are equal.
    Order of records or columns does not matter.
    
    Parameters
    ----------
    d1 : Mapping[str, Sequence]
        data mapping of {column name: column values}
    d2 : Mapping[str, Sequence]
        data mapping of {column name: column values}
    
    Examples
    --------
    >>> d1 = {'x': [1, 2, 3, 4], 'y': [55, 66, 77, 88]}
    >>> d2 = {'x': [2, 1, 4, 3], 'y': [66, 55, 88, 77]}
    >>> records_equal(d1, d2)
    True
    
    >>> d1 = {'x': [1, 2, 3, 4], 'y': [55, 66, 77, 88]}
    >>> d2 = {'x': [2, 1, 4, 3], 'y': [55, 77, 88, 66]}
    >>> records_equal(d1, d2)
    False
    """
    if set(data_features.column_names(d1)) != set(data_features.column_names(d2)):
        return False
    
    if data_features.row_count(d1) != data_features.row_count(d2):
        return False
    
    d2_rows = [row for row in records(d2)]
    
    for row in records(d1):
        if row in d2_rows:
            d2_rows.remove(row)
        else:
            return False
    
    return True