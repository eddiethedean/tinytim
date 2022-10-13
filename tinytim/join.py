from typing import Optional
from tinytim.filter import filter_list_by_indexes


def locate(l: list, value) -> list[int]:
    """Return list of all index of each matching item in list."""
    return [i for i, x in enumerate(l) if x == value]


def matching_indexes(l1, l2) -> tuple[tuple[int], tuple[int]]:
    """
    Find matching item value indexes in two lists.
    
    Example
    -------
    >>> l1 = [1, 3, 4, 6, 1]
    >>> l2 = [1, 2, 3, 4, 3]
    >>> matching_indexes(l1, l2)
    ((0, 4, 1, 2, 1), (0, 2, 4, 3, 0))
    """
    l1_indexes = []
    l2_indexes = []
    out = []
    for value in l1:
        l1_indexes.extend(locate(l2, value))
    for value in l2:
        l2_indexes.extend(locate(l1, value))
    return tuple(l2_indexes), tuple(l1_indexes)


def inner_join(left: dict,
               right: dict,
               left_on: str,
               right_on: Optional[str] = None,
               select: Optional[list[str]] = None
) -> dict:
    """
    Inner Join two data dict on a specified column name(s).
    If right_on is None, joins both on same column name (left_on).
    Parameters
    ----------
    left : Mapping[str, Sequence]
        left data mapping of {column name: column values}
    right : Mapping[str, Sequence]
        right data mapping of {column name: column values}
    left_on : str
        column name to join on in left
    right_on : str, optional
        column name to join on in right, join on left_on if None
    select : list[str], optional
        column names to return
        
    Example
    -------
    >>> left = {'id': [1, 3, 4, 6], 'x': [33, 44, 55, 66, 77]}
    >>> right = {'id': [1, 2, 3, 4], 'y': [11, 22, 33, 44]}
    >>> inner_join(left, right, 'id')
    {'id': [1, 3, 4], 'x': [33, 44, 55], 'y': [11, 33, 44]}
    """
    # check if on1 and on2 are in column names
    right_on = left_on if right_on is None else right_on
    if left_on not in left:
        raise ValueError(f'column {left_on} is missing from left table')
    if right_on not in right:
        raise ValueError(f'column {right_on} is missing from right table')
        
    # find indexes where on1 and on2 match
    left_indexes, right_indexes = matching_indexes(left[left_on], right[right_on])
    
    out = {}
    
    for key in left:
        out[key] = filter_list_by_indexes(left[key], left_indexes)
    for key in right:
        out[key] = filter_list_by_indexes(right[key], right_indexes)
    
    if select is not None:
        return {col: out[col] for col in select}
    return out
