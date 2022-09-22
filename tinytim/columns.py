from typing import Dict, Generator, Iterable, Mapping, Sequence, Tuple

import tinytim.data as data_features
from dictanykey import DefaultDictAnyKey, DictAnyKey

DataMapping = Mapping[str, Sequence]


def column_dict(data: DataMapping, col: str) -> Dict[str, Sequence]:
    """
    Return a dict of {col_name, col_values} from data.
        
    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    col : str
        column name to pull out of data.

    Returns
    -------
    dict[str, Sequence]
        {column_name: column_values}

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> column_dict(data, 'x')
    {'x': [1, 2, 3]}
    >>> column_dict(data, 'y')
    {'y': [6, 7, 8]}
    """
    return {col: data_features.column_values(data, col)}


def itercolumns(data: DataMapping) -> Generator[Tuple[str, tuple], None, None]:
    """
    Return a generator of tuple column name, column values.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    
    Returns
    -------
    Generator[Tuple[str, tuple], None, None]
        generator that yields tuples(column_name, column_values)
        
    Example
    -------
    >>> data = 'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> cols = list(itercolumns(data))
    >>> cols[0]
    ('x', (1, 2, 3)) 
    >>> cols[1]
    ('y', (6, 7, 8))
    """
    for col in data_features.column_names(data):
        yield col, tuple(data_features.column_values(data, col))


def value_counts(
   values: Iterable,
   sort=True,
   ascending=True
) -> DictAnyKey:
    """
    Count up each value.
    Return a DictAnyKey[value] -> count
    Allows for unhashable values.

    Parameters
    ----------
    values :
        values to be counted up
    sort : default True, sort results by counts
    ascending: default True, sort highest to lowest


    Returns
    -------
    DictAnyKey[Any, int]
        {value: value_count}

    Example
    -------
    >>> values = [4, 1, 1, 4, 5, 1]
    >>> value_counts(values)
    DictAnyKey((1, 3), (4, 2), (5, 1))
    """
    d = DefaultDictAnyKey(int)
    for value in values:
        d[value] += 1
    if sort:
        return DictAnyKey(sorted(d.items(),  # type: ignore
                                 key=lambda item: item[1],  # type: ignore
                                 reverse=ascending))
    else:
        return DictAnyKey(d)