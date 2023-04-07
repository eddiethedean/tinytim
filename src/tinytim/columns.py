"""Description: Functions for operating on columns of data."""

from typing import Generator, Tuple

import tinytim.data as data_functions
from tinytim.custom_types import DataDict
from tinytim.interfaces import GetSequence, KeyNamesGetSequence
from tinytim.sequences import add_to_sequence, divide_sequence, exponent_sequence
from tinytim.sequences import floor_sequence, mod_sequence, multiply_sequence
from tinytim.sequences import operate_on_sequence, subtract_from_sequence

operate_on_column = operate_on_sequence
add_to_column = add_to_sequence
subtract_from_column = subtract_from_sequence
multiply_column = multiply_sequence
divide_column = divide_sequence
mod_column = mod_sequence
exponent_column = exponent_sequence
floor_column = floor_sequence


def column_mapping(data: GetSequence, col: str) -> DataDict:
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
    return {col: data_functions.column_values(data, col)}


def itercolumns(data: KeyNamesGetSequence) -> Generator[Tuple[str, list], None, None]:
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
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> generator = itercolumns(data)
    >>> next(generator)
    ('x', (1, 2, 3)) 
    >>> next(generator)
    ('y', (6, 7, 8))
    """
    for col in data_functions.column_names(data):
        yield col, data_functions.column_values(data, col)