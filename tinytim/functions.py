from collections import defaultdict, namedtuple
import copy
import random
from typing import Any, Callable, Collection, Generator, Iterable, List, Optional
from typing import Dict, Mapping, MutableMapping, MutableSequence, Tuple, Union, Sequence


TableFilter = Iterable[bool]


def column_filter(column: Iterable, func: Callable) -> List[bool]:
    return [func(item) for item in column]


def indexes_from_filter(f: TableFilter) -> List[int]:
    return [i for i, b in enumerate(f) if b]


def filter_list_by_indexes(values: Sequence, indexes: Sequence[int]) -> List:
    """Return only values in indexes."""
    return [values[i] for i in indexes]


def filter_by_indexes(data: MutableMapping, indexes: Sequence[int]) -> dict:
    """Return only rows in indexes"""
    return {col: filter_list_by_indexes(values, indexes) for col, values in data.items()}


def filter_data(data: MutableMapping, f: TableFilter) -> dict:
    indexes = indexes_from_filter(f)
    return filter_by_indexes(data, indexes)


def filter_by_column_func(data: MutableMapping, column_name: str, func) -> dict:
    """Return only rows of data where named column equals value."""
    indexes = [i for i, val in enumerate(data[column_name]) if func(val)]
    return filter_by_indexes(data, indexes)


def filter_by_column_eq(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column equals value."""
    return filter_by_column_func(data, column_name, lambda x: x == value)


def filter_by_column_ne(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column does not equal value."""
    return filter_by_column_func(data, column_name, lambda x: x != value)


def filter_by_column_gt(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column is greater than value."""
    return filter_by_column_func(data, column_name, lambda x: x > value)


def filter_by_column_lt(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column is less than value."""
    return filter_by_column_func(data, column_name, lambda x: x < value)


def filter_by_column_ge(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column is greater than or equal value."""
    return filter_by_column_func(data, column_name, lambda x: x >= value)


def filter_by_column_le(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column is less than or equal value."""
    return filter_by_column_func(data, column_name, lambda x: x <= value)


def filter_by_column_isin(data: MutableMapping, column_name: str, values) -> dict:
    """Return only rows of data where named column is in values."""
    return filter_by_column_func(data, column_name, lambda x: x in values)


def filter_by_column_notin(data: MutableMapping, column_name: str, values) -> dict:
    """Return only rows of data where named column is not in values."""
    return filter_by_column_func(data, column_name, lambda x: x not in values)


def groupbycolumn(data: MutableMapping, column: Collection) -> List[tuple]:
    keys = uniques(column)
    return [(k, filter_data(data, column_filter(column, lambda x: x == k)))
                for k in keys]


def groupbyone(data: MutableMapping, column_name: str) -> List[tuple]:
    return groupbycolumn(data, data[column_name])


def row_value_tuples(data: MutableMapping, column_names: Collection[str]) -> List[tuple]:
    return list(zip(*[data[col] for col in column_names]))


def groupbymulti(data: MutableMapping, column_names: Collection[str]) -> List[tuple]:
    return groupbycolumn(data, row_value_tuples(data, column_names))


def groupby(data: MutableMapping, by: Union[str, Collection[str]]) -> List[tuple]:
    if isinstance(by, str):
        return groupbyone(data, by)
    else:
        return groupbymulti(data, by)


def _keys(key, by) -> dict:
    keys = {}
    if isinstance(by, str):
        keys[by] = key
    else:
        for col, k in zip(by, key):
            keys[col] = k
    return keys


def aggregate_groups(groups: List[tuple], by: Collection[str], func: Callable, tuplename: str) -> Tuple[List, dict]:
    labels = []
    rows = []
    for key, data in groups:
        row = func(data)
        if len(row):
            GroupbyKey = namedtuple(field_names=by, typename='GroupbyKey')
            keys = _keys(key, by)
            labels.append(GroupbyKey(*keys.values()))
            rows.append(row)
    return labels, row_dicts_to_data(rows)


def sum_groups(groups: List[tuple], by: Collection[str]) -> Tuple[List, dict]:
    return aggregate_groups(groups, by, sum_data, 'Sums')


def count_groups(groups: List[tuple], by: Collection[str]) -> Tuple[List, dict]:
    return aggregate_groups(groups, by, count_data, 'Counts')


def aggregate_data(data: MutableMapping, func: Callable) -> dict:
    out = {}
    for column_name in data.keys():
        try:
            col_sum = func(data[column_name])
        except TypeError:
            continue
        out[column_name] = col_sum
    return out


def sum_data(data: MutableMapping) -> dict:
    return aggregate_data(data, sum)


def count_data(data: MutableMapping) -> dict:
    return aggregate_data(data, len)


def edit_row_items_inplace(data: MutableMapping, index: int, items: Mapping) -> None:
    """Changes row index to mapping items values."""
    for col in items:
        data[col][index] = items[col]


def edit_row_values_inplace(data: MutableMapping, index: int, values: MutableSequence) -> None:
    """Changed row index to values."""
    if len(values) != column_count(data):
        raise AttributeError('values length must match columns length.')
    for col, value in zip(column_names(data), values):
        data[col][index] = value


def edit_column_inplace(data: MutableMapping, column_name: str, values: MutableSequence) -> None:
    """Add values to data in named column.
       Overrides existing values if column exists,
       Created new column with values if column does not exist.
    """
    if len(values) != row_count(data):
        raise ValueError('values length must match data rows count.')
    data[column_name] = values


def drop_row_inplace(data: MutableMapping, index: int) -> None:
    """Remove index row from data."""
    for col in column_names(data):
        data[col].pop(index)


def drop_label_inplace(labels: Union[None, List], index) -> None:
    if labels is not None:
        labels.pop(index)


def drop_column_inplace(data: MutableMapping, column_name: str) -> None:
    """Return a new dict with the named column removed from data."""
    del data[column_name]


def edit_value_inplace(data: MutableMapping, column_name: str, index: int, value: Any) -> None:
    """Edit the value in named column as row index."""
    data[column_name][index] = value


def column_count(data: MutableMapping) -> int:
    """Return the number of columns in data."""
    return len(data)


def row_count(data: MutableMapping) -> int:
    """Return the number of rows in data."""
    if column_count(data) == 0: return 0
    return len(data[first_column_name(data)])


def shape(data: MutableMapping) -> Tuple[int, int]:
    """Return data row count, column count tuple."""
    col_count = column_count(data)
    if col_count == 0: return 0, 0
    return row_count(data), col_count


def size(data: MutableMapping) -> int:
    """Return data row count multiplied by column count."""
    rows, columns = shape(data)
    return rows * columns


def first_column_name(data: MutableMapping) -> str:
    """Return the name of the first column.
       Raises StopIteration if data has zero columns.
    """
    return next(iter(data))


def column_names(data: MutableMapping) -> Tuple[str]:
    """Return data column names."""
    return tuple(data)


def replace_column_names(data: MutableMapping, new_names: MutableSequence[str]) -> dict:
    """Return a new dict same column data but new column names."""
    old_names = column_names(data)
    if len(new_names) != len(old_names):
        raise ValueError('new_names must be same size as data column_count.')
    return {new_name: data[old_name] for new_name, old_name in zip(new_names, old_names)}


def index(data: MutableMapping) -> Tuple[int]:
    """Return tuple of data column indexes."""
    return tuple(range(row_count(data)))


def data_columns_same_len(data: MutableMapping) -> bool:
    """Check if data columns are all the same len."""
    if column_count(data) == 0: return True
    it = iter(data.values())
    the_len = len(next(it))
    return all(len(l) == the_len for l in it)


def valid_table_mapping(data: MutableMapping) -> bool:
    """Check if data is a true TableMapping."""
    if not has_mapping_attrs(data): return False
    return data_columns_same_len(data)


def table_value(data: MutableMapping, column_name: str, index: int) -> Any:
    """Return one value from column at row index."""
    return data[column_name][index]


def row_dict(data: MutableMapping, index: int) -> dict: 
    """Return one row from data at index."""
    return {col: table_value(data, col, index) for col in column_names(data)}


def row_values(data: MutableMapping, index: int) -> tuple:
    """Return a tuple of the values at row index."""
    return tuple(values[index] for values in data.values())


def column_dict(data, col: str) -> Dict[str, MutableSequence]:
    return {col: data[col]}


def column_values(data: MutableMapping, column_name: str) -> MutableSequence:
    return data[column_name]


def itercolumns(data: MutableMapping) -> Generator[Tuple[str, tuple], None, None]:
    """Return a generator of tuple column name, column values."""
    for col in column_names(data):
        yield col, tuple(data[col])
            

def iterrows(data: MutableMapping) -> Generator[Tuple[int, dict], None, None]:
    """Return a generator of tuple row index, row dict values."""
    for i in index(data):
        yield i, row_dict(data, i)


def itertuples(data: MutableMapping) -> Generator[tuple, None, None]:
    """Return a generator of tuple index and row values."""
    for i, row in iterrows(data):
        yield i, *row.values()


def itervalues(data: MutableMapping) -> Generator[tuple, None, None]:
    """Return a generator of tuple row values."""
    for i, row in iterrows(data):
        yield tuple(row.values())


def values(data: MutableMapping) -> Tuple[tuple]:
    """Return tuple of tuple row values."""
    return tuple(itervalues(data))


def only_columns(data: MutableMapping, column_names: MutableSequence[str]) -> dict:
    """Return new TableDict with only column_names."""
    return {col: data[col] for col in column_names}


def sample(data: MutableMapping, n: int, random_state: Optional[int] = None) -> dict:
    """return random sample of n rows"""
    if random_state is not None:
        random.seed(random_state)
    indexes = random.sample(range(row_count(data)), n)
    return filter_by_indexes(data, indexes)


def sample_indexes(data: MutableMapping, n: int, random_state: Optional[int] = None) -> List[int]:
    """return random sample of n indexes"""
    if random_state is not None:
        random.seed(random_state)
    return random.sample(range(row_count(data)), n)


def nunique(data: MutableMapping) -> Dict[str, int]:
    """Count number of distinct values in each column.
       Return dict with number of distinct values.
    """
    return {col: len(uniques(values)) for col, values in data.items()}


def head(data: MutableMapping, n: int = 5) -> dict:
    """Return the first n rows of data."""
    return {col: values[:n] for col, values in data.items()}


def tail(data: MutableMapping, n: int = 5) -> dict:
    """Return the last n rows of data."""
    return {col: values[-n:] for col, values in data.items()}


def edit_row_items(data: MutableMapping, index: int, items: Mapping) -> MutableMapping:
    """Return a new dict with row index changed to mapping items values."""
    new_data = copy.copy(data)
    edit_row_items_inplace(new_data, index, items)
    return new_data


def edit_row_values(data: MutableMapping, index: int, values: MutableSequence) -> MutableMapping:
    """Return a new dict with row index changed to values."""
    new_data = copy_table(data)
    edit_row_values_inplace(new_data, index, values)
    return new_data


def edit_column(data: MutableMapping, column_name: str, values: MutableSequence) -> MutableMapping:
    """Returns a new dict with values added to data in named column.
       Overrides existing values if column exists,
       Created new column with values if column does not exist.
    """
    new_data = copy_table(data)
    edit_column_inplace(data, column_name, values)
    return new_data


def edit_value(data: MutableMapping, column_name: str, index: int, value: Any) -> MutableMapping:
    """Return a new table with the value in named column changed at row index."""
    new_data = copy_table(data)
    edit_value_inplace(data, column_name, index, value)
    return new_data


def drop_row(data: MutableMapping, index: int) -> MutableMapping:
    """Return a new dict with index row removed from data."""
    new_data = copy_table(data)
    drop_row_inplace(data, index)
    return new_data


def drop_label(labels: Union[None, List], index: int) -> Union[None, List]:
    new_labels = copy.copy(labels)
    drop_label_inplace(new_labels, index)
    return new_labels


def drop_column(data: MutableMapping, column_name: str) -> MutableMapping:
    """Return a new dict with the named column removed from data."""
    new_data = copy_table(data)
    drop_column_inplace(data, column_name)
    return new_data


def copy_table(data: MutableMapping) -> MutableMapping:
    return copy.copy(data)


def deepcopy_table(data: MutableMapping) -> MutableMapping:
    return copy.deepcopy(data)


def combine_names_rows(column_names, rows) -> Dict[str, List]:
    return dict(zip(column_names, map(list, zip(*rows))))


def agg_data_to_data(agg_data: dict) -> dict:
    """Convert aggregated data to dict table."""
    first_value = next(iter(agg_data.values()))
    column_names = first_value._fields
    return combine_names_rows(column_names, agg_data.values())


def add_data_to_labels(agg_data: dict) -> dict:
    first_value = next(iter(agg_data.keys()))
    column_names = first_value._fields
    return combine_names_rows(column_names, agg_data.keys())


def uniques(values: Iterable) -> List:
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


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


def row_values_generator(row: Mapping) -> Generator[Any, None, None]:
    for key in row:
        yield row[key]