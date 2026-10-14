import tinytim.data as data_functions
from tinytim.custom_types import DataMapping
from tinytim.utils import has_mapping_attrs


def data_columns_same_len(data: DataMapping) -> bool:
    """Check if data columns are all the same len."""
    if data_functions.column_count(data) == 0:
        return True
    it = iter(data.values())
    the_len = len(next(it))
    return all(len(col) == the_len for col in it)


def valid_table_mapping(data: DataMapping) -> bool:
    """Check if data is a true TableMapping."""
    if not has_mapping_attrs(data):
        return False
    return data_columns_same_len(data)
