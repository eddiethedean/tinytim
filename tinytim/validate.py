from typing import MutableMapping

from tinytim.features import column_count
from tinytim.utils import has_mapping_attrs


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