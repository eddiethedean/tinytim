from typing import Any, Mapping, Optional, Union


def fillna(
    data: Mapping,
    value: Optional[Any] = None,
    method: Optional[str] = None,
    axis: Optional[int] = None,
    unplace: bool = False,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> Union[Mapping, None]:
    """
    Fill missing values using the specified method.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    value : Any
        value to use to fill missing values
    method : {'backfill', 'bfill', 'pad', 'ffill', None}
        method to use for filling holes in reindexed
        Series.
        pad/ffill: propagate last valid observation
        forward to next valid
        backfill/bfill: use next valid observation to fill gap.

    Returns
    -------
    Mapping or None
        Object with missing values filled or None if inplace=True
    """
    ...


def back