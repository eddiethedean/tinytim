from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import Any

from tinytim.interfaces import SequenceItems

DataMapping = Mapping[str, Sequence[Any]]
MutableDataMapping = MutableMapping[str, MutableSequence[Any]]
RowMapping = Mapping[str, Any]
DataDict = dict[str, list[Any]]
RowDict = dict[str, Any]


def data_dict(m: SequenceItems) -> DataDict:
    return {str(col): list(values) for col, values in m.items()}


def row_dict(m: SequenceItems) -> RowDict:
    return {str(col): value for col, value in m.items()}
