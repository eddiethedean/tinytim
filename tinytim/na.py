from typing import Any, Mapping, MutableMapping, MutableSequence, Optional, Union


def fillna(
    data: Mapping,
    value: Optional[Any] = None,
    method: Optional[str] = None,
    axis: Optional[int] = None,
    inplace: bool = False,
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


def fill_with_value(
    data: Mapping,
    value: Optional[Any] = None,
    axis: Optional[int] = None,
    inplace: bool = False,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> Union[Mapping, None]:
    """
    Fill data columns with given value.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    value : Any
        value to use to fill missing values
        If value is Mapping: {column_name: value},
        fill missing values in each column with each value.
    """


def fill_column_with_value(
    column: MutableSequence,
    value: Optional[Any] = None,
    inplace: bool = False,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> Union[MutableSequence, None]:
    """
    Fill missing values in column with given value.

    Parameters
    ----------
    column : MutableSequence
        column of values
    value : Any
        value to use to fill missing values
    inplace : bool, default False
        return MutableSequence if False,
        return None if True and change column inplace
    limit : int, default None
        max number of values to fill, fill all if None
    na_value : Any, default None
        value to replace, use np.nan for pandas DataFrame
    
    Returns
    -------
    MutableSequence | None

    Examples
    --------
    >>> col = [1, None, 3, None, 5]
    >>> fill_column_with_value(col, 0)
    [1, 0, 3, 0, 5]
    >>> col
    [1, None, 3, None, 5]

    >>> col = [1, None, 3, None, 5]
    >>> fill_column_with_value(col, 0, inplace=True)
    >>> col
    [1, 0, 3, 0, 5]
    """


def fill_row_with_value(
    column: MutableMapping,
    value: Optional[Any] = None,
    inplace: bool = False,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> Union[MutableSequence, None]:
    """
    Fill missing values in row with given value.

    Parameters
    ----------
    row : MutableMapping
        row of values: {column_name: row_value}
    value : Any
        value to use to fill missing values
    inplace : bool, default False
        return MutableSequence if False,
        return None if True and change column inplace
    limit : int, default None
        max number of values to fill, fill all if None
    na_value : Any, default None
        value to replace, use np.nan for pandas DataFrame
    
    Returns
    -------
    MutableSequence | None

    Examples
    --------
    >>> col = [1, None, 3, None, 5]
    >>> fill_column_with_value(col, 0)
    [1, 0, 3, 0, 5]
    >>> col
    [1, None, 3, None, 5]

    >>> col = [1, None, 3, None, 5]
    >>> fill_column_with_value(col, 0, inplace=True)
    >>> col
    [1, 0, 3, 0, 5]
    """