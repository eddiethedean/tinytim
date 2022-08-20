from collections import defaultdict
from typing import Any, Collection, Dict, Generator, Iterable, List, Mapping, MutableMapping, Optional


def uniques(values: Iterable) -> List:
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def row_value_tuples(data: MutableMapping, column_names: Collection[str]) -> List[tuple]:
    return list(zip(*[data[col] for col in column_names]))


def _keys(key, by) -> dict:
    keys = {}
    if isinstance(by, str):
        keys[by] = key
    else:
        for col, k in zip(by, key):
            keys[col] = k
    return keys


def row_dicts_to_data(rows: List[dict]) -> dict:
    keys = all_keys(rows)
    data = defaultdict(list)
    for row in rows:
        for col in keys:
            if col in row:
                data[col].append(row[col])
            else:
                data[col].append(None)
    return dict(data)


def all_bool(l: List) -> bool:
    return all(isinstance(item, bool) for item in l)


def has_mapping_attrs(obj: Any) -> bool:
    """Check if object has all Mapping attrs."""
    mapping_attrs = ['__getitem__', '__iter__', '__len__',
                     '__contains__', 'keys', 'items', 'values',
                     'get', '__eq__', '__ne__']
    return all(hasattr(obj, a) for a in mapping_attrs)


def all_keys(dicts: List[dict]) -> List:
    keys = []
    for d in dicts:
        for key in d:
            if key not in keys:
                keys.append(key)
    return keys


def row_values_generator(row: Mapping) -> Generator[Any, None, None]:
    for key in row:
        yield row[key]


def slice_to_range(s: slice, stop: Optional[int] = None) -> range:
    """Convert an int:int:int slice object to a range object.
       Needs stop if s.stop is None since range is not allowed to have stop=None.
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


def combine_names_rows(column_names, rows) -> Dict[str, List]:
    return dict(zip(column_names, map(list, zip(*rows))))


def nunique(data: MutableMapping) -> Dict[str, int]:
    """Count number of distinct values in each column.
       Return dict with number of distinct values.
    """
    return {col: len(uniques(values)) for col, values in data.items()}