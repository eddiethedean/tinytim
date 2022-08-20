import copy
import random
from typing import Any, List, MutableMapping, MutableSequence, Generator, Optional, Mapping, Union

import tinytim.functional.utils as utils
import tinytim.functional.inplace as inplace


def column_count(data: MutableMapping) -> int:
    """Return the number of columns in data."""
    return len(data)


def row_count(data: MutableMapping) -> int:
    """Return the number of rows in data."""
    if column_count(data) == 0: return 0
    return len(data[first_column_name(data)])


def shape(data: MutableMapping) -> tuple[int, int]:
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


def column_names(data: MutableMapping) -> tuple[str]:
    """Return data column names."""
    return tuple(data)


def replace_column_names(data: MutableMapping, new_names: MutableSequence[str]) -> dict:
    """Return a new dict same column data but new column names."""
    old_names = column_names(data)
    if len(new_names) != len(old_names):
        raise ValueError('new_names must be same size as data column_count.')
    return {new_name: data[old_name] for new_name, old_name in zip(new_names, old_names)}


def index(data: MutableMapping) -> tuple[int]:
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
    if not utils.has_mapping_attrs(data): return False
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


def column_dict(data, col: str) -> dict[str, MutableSequence]:
    return {col: data[col]}


def column_values(data: MutableMapping, column_name: str) -> MutableSequence:
    return data[column_name]


def itercolumns(data: MutableMapping) -> Generator[tuple[str, tuple], None, None]:
    """Return a generator of tuple column name, column values."""
    for col in column_names(data):
        yield col, tuple(data[col])
            

def iterrows(data: MutableMapping) -> Generator[tuple[int, dict], None, None]:
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


def values(data: MutableMapping) -> tuple[tuple]:
    """Return tuple of tuple row values."""
    return tuple(itervalues(data))


def filter_by_indexes(data: MutableMapping, indexes: MutableSequence[int]) -> dict:
    """return only rows in indexes"""
    return {col: [values[i] for i in indexes] for col, values in data.items()}


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


def nunique(data: MutableMapping) -> dict[str, int]:
    """Count number of distinct values in each column.
       Return dict with number of distinct values.
    """
    return {col: len(utils.uniques(values)) for col, values in data.items()}


def head(data: MutableMapping, n: int = 5) -> dict:
    """Return the first n rows of data."""
    return {col: values[:n] for col, values in data.items()}


def tail(data: MutableMapping, n: int = 5) -> dict:
    """Return the last n rows of data."""
    return {col: values[-n:] for col, values in data.items()}


def edit_row_items(data: MutableMapping, index: int, items: Mapping) -> MutableMapping:
    """Return a new dict with row index changed to mapping items values."""
    new_data = copy.copy(data)
    inplace.edit_row_items(new_data, index, items)
    return new_data


def edit_row_values(data: MutableMapping, index: int, values: MutableSequence) -> MutableMapping:
    """Return a new dict with row index changed to values."""
    new_data = copy_table(data)
    inplace.edit_row_values(new_data, index, values)
    return new_data


def edit_column(data: MutableMapping, column_name: str, values: MutableSequence) -> MutableMapping:
    """Returns a new dict with values added to data in named column.
       Overrides existing values if column exists,
       Created new column with values if column does not exist.
    """
    new_data = copy_table(data)
    inplace.edit_column(data, column_name, values)
    return new_data


def edit_value(data: MutableMapping, column_name: str, index: int, value: Any) -> MutableMapping:
    """Return a new table with the value in named column changed at row index."""
    new_data = copy_table(data)
    inplace.edit_value(data, column_name, index, value)
    return new_data


def drop_row(data: MutableMapping, index: int) -> MutableMapping:
    """Return a new dict with index row removed from data."""
    new_data = copy_table(data)
    inplace.drop_row(data, index)
    return new_data


def drop_label(labels: Union[None, List], index: int) -> Union[None, List]:
    new_labels = copy.copy(labels)
    inplace.drop_label(new_labels, index)
    return new_labels


def drop_column(data: MutableMapping, column_name: str) -> MutableMapping:
    """Return a new dict with the named column removed from data."""
    new_data = copy_table(data)
    inplace.drop_column(data, column_name)
    return new_data


def copy_table(data: MutableMapping) -> MutableMapping:
    return copy.copy(data)


def deepcopy_table(data: MutableMapping) -> MutableMapping:
    return copy.deepcopy(data)