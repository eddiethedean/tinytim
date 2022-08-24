import copy
from typing import List, MutableMapping


def copy_table(data: MutableMapping) -> MutableMapping:
    return copy.copy(data)


def deepcopy_table(data: MutableMapping) -> MutableMapping:
    return copy.deepcopy(data)


def copy_list(values: List) -> List:
    return copy.copy(values)


def deepcopy_list(values: List) -> List:
    return copy.deepcopy(values)