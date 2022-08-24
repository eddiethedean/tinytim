from typing import MutableMapping

import tinytim.data as data_features
import tinytim.utils as utils


def data_columns_same_len(data: MutableMapping) -> bool:
    """Check if data columns are all the same len."""
    if data_features.column_count(data) == 0: return True
    it = iter(data.values())
    the_len = len(next(it))
    return all(len(l) == the_len for l in it)


def valid_table_mapping(data: MutableMapping) -> bool:
    """Check if data is a true TableMapping."""
    if not utils.has_mapping_attrs(data): return False
    return data_columns_same_len(data)