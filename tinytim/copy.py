import copy
from typing import List, MutableMapping


def copy_table(data: MutableMapping) -> MutableMapping:
    return copy.deepcopy(data)


def deepcopy_table(data: MutableMapping) -> dict:
    return {col: copy.deepcopy(values) for col, values in data.items()}


def copy_list(values: List) -> List:
    return copy.copy(values)


def deepcopy_list(values: List) -> List:
    return copy.deepcopy(values)