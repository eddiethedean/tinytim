from collections import defaultdict
from typing import Any, Collection, Dict, Generator, Iterable, List, Mapping
from typing import MutableMapping, Optional, Sequence, Tuple


def uniques(values: Iterable) -> List:
    """Return a list of the unique items in values.

       Examples:
       values = [1, 1, 2, 4, 5, 2, 0, 6, 1]
       uniques(values) -> [1, 2, 4, 5, 0, 6]
    """
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def row_value_tuples(data: MutableMapping, column_names: Collection[str]) -> Tuple[tuple]:
    """Return row value tuples for only columns in column_names.

       data = {'x': [1, 2, 3], 'y': [6, 7, 8], 'z': [9, 10, 11]}
       row_value_tuples(data, ['x', 'z']) -> ((1, 9), (2, 10), (3, 11))
    """
    return tuple(zip(*[data[col] for col in column_names]))


def _keys(key, by) -> dict:
    keys = {}
    if isinstance(by, str):
        keys[by] = key
    else:
        for col, k in zip(by, key):
            keys[col] = k
    return keys


def row_dicts_to_data(rows: Collection[dict], missing_value=None) -> Dict[str, list]:
    """Convert a list of row dicts to dict[col_name: values] format.

       Examples:
       rows = [{'x': 1, 'y': 20}, {'x': 2, 'y': 21}, {'x': 3, 'y': 22}]
       row_dicts_to_data(rows) -> {'x': [1, 2, 3], 'y': [20, 21, 22]}

       rows = [{'x': 1, 'y': 20}, {'x': 2}, {'x': 3, 'y': 22}]
       row_dicts_to_data(rows) -> {'x': [1, 2, 3], 'y': [20, None, 22]}
    """
    keys = all_keys(rows)
    data = defaultdict(list)
    for row in rows:
        for col in keys:
            if col in row:
                data[col].append(row[col])
            else:
                data[col].append(missing_value)
    return dict(data)


def all_bool(values: Collection) -> bool:
    """Return if all items in values are bool or not.
       
       Examples:
       values = [1, True, False, True]
       all_bool(values) -> False

       values = [True, True, False, True]
       all_bool(values) -> True
    """
    return all(isinstance(item, bool) for item in values)


def has_mapping_attrs(obj: Any) -> bool:
    """Check if object has all Mapping attrs.
    
       Examples:
       obj = dict()
       has_mapping_attrs(obj) -> True

       obj = list()
       has_mapping_attrs(obj) -> False
    """
    mapping_attrs = ['__getitem__', '__iter__', '__len__',
                     '__contains__', 'keys', 'items', 'values',
                     'get', '__eq__', '__ne__']
    return all(hasattr(obj, a) for a in mapping_attrs)


def all_keys(dicts: Collection[dict]) -> List:
    """Return all the unique keys from a collection of dicts.
    
       Examples:
       dicts = [{'x': 1, 'y': 2}, {'x': 4, 'z': 7}]
       all_keys(dicts) -> ['x', 'y', 'z']
    """
    keys = []
    for d in dicts:
        for key in d:
            if key not in keys:
                keys.append(key)
    return keys


def row_values_generator(row: Mapping) -> Generator[Any, None, None]:
    """Return a generator that yields values from a row dict.
       
       Examples:
       row = {'x': 1, 'y': 4, 'z': 8}
       generator = row_values_generator(row)
       next(generator) -> 1
       next(generator) -> 4
       next(generator) -> 8
       next(generator) -> StopIteration
    """
    for key in row:
        yield row[key]


def slice_to_range(s: slice, stop: Optional[int] = None) -> range:
    """Convert an int:int:int slice object to a range object.
       Needs stop if s.stop is None since range is not allowed to have stop=None.

       Examples:
       s = slice(1, 4, 0)
       slice_to_range(s) -> ValueError

       s = slice(0, 3, 1)
       slice_to_range(s) -> range(0, 3, 1)
    """
    step = 1 if s.step is None else s.step
    if step == 0:
        raise ValueError('step must not be zero')

    if step > 0:
        start = 0 if s.start is None else s.start
        stop = s.stop if s.stop is not None else stop
    else:
        start = stop if s.start is None else s.start
        if isinstance(start, int):
            start -= 1
        stop = -1 if s.stop is None else s.stop

        if start is None:
            raise ValueError('start cannot be None is range with negative step')

    if stop is None:
        raise ValueError('stop cannot be None in range')
    
    return range(start, stop, step)


def combine_names_rows(column_names: Sequence, rows: Sequence) -> Dict[str, List]:
    """Convert a sequence of column names and a sequence of row values into dict[column_name: values] format.

       Examples:
       column_names = ['x', 'y']
       rows = ((1, 2), (4, 5), (8, 10))
       combine_names_rows(column_names, rows) -> {'x': [1, 4, 8], 'y': [2, 5, 10]}
    """
    return dict(zip(column_names, map(list, zip(*rows))))


def nunique(data: MutableMapping) -> Dict[str, int]:
    """Count number of distinct values in each column.
       Return dict with number of distinct values.

       Examples:
       data = {'x': [1, 2, 2], 'y': [6, 7, 8], 'z': [9, 9, 9]}
       nunique(data) -> {'x': 2, 'y': 3, 'z': 1}
    """
    return {col: len(uniques(values)) for col, values in data.items()}