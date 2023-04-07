from typing import Any, Dict, Mapping, Sequence, MutableMapping, MutableSequence

from tinytim.interfaces import SequenceItems

DataMapping = Mapping[str, Sequence]
MutableDataMapping = MutableMapping[str, MutableSequence]
RowMapping = Mapping[str, Any]
DataDict = Dict[str, list]
RowDict = Dict[str, Any]


def data_dict(m: SequenceItems) -> DataDict:
    return {str(col): list(values) for col, values in m.items()}


def row_dict(m: SequenceItems) -> RowDict:
    return {str(col): value for col, value in m.items()}