User guide
==========

Tables
------

TinyTim stores a table as a mapping from each column name to its values. For
example:

.. code-block:: python

   data = {"name": ["Ada", "Lin"], "score": [95, 88]}

Every column should have the same number of values. Use
:func:`tinytim.validate.valid_table_mapping` to check a table. The
:mod:`tinytim.data` module provides helpers such as :func:`tinytim.data.shape`,
:func:`tinytim.data.row_count`, and :func:`tinytim.data.column_names`.

Most operations return new data. Functions ending in ``_inplace`` modify the
table passed to them.

Rows and columns
----------------

Use :func:`tinytim.rows.row_dict` to read a row as a dictionary, or
:func:`tinytim.rows.iterrows` to iterate over rows:

.. code-block:: python

   from tinytim.rows import iterrows, row_dict

   row_dict(data, 0)
   # {'name': 'Ada', 'score': 95}

   list(iterrows(data))
   # [(0, {'name': 'Ada', 'score': 95}), (1, {'name': 'Lin', 'score': 88})]

Use :func:`tinytim.edit.edit_column` to replace or add a column. The new
column must have one value per row:

.. code-block:: python

   from tinytim.edit import edit_column

   edit_column(data, "passed", [True, True])
   # {'name': ['Ada', 'Lin'], 'score': [95, 88], 'passed': [True, True]}

Filtering and grouping
----------------------

Filter rows with functions such as :func:`tinytim.filter.filter_by_column_gt`
and :func:`tinytim.filter.filter_by_column_isin`. Group a table by one or more
columns with :func:`tinytim.group.groupby`:

.. code-block:: python

   from tinytim.group import groupby, sum_groups

   data = {"team": ["A", "B", "A"], "points": [4, 3, 5]}
   labels, totals = sum_groups(groupby(data, "team"))
   # labels: ['A', 'B']
   # totals: {'points': [9, 3]}

Missing values
--------------

Missing values are ``None`` by default. :func:`tinytim.na.isna` builds a
missing-value mask, :func:`tinytim.na.dropna` removes rows or columns, and
:func:`tinytim.na.fillna` fills missing entries. Pass ``na_value`` when a
different marker represents missing data.

.. code-block:: python

   from tinytim.na import dropna, fillna, isna

   data = {"score": [10, None, None, 20]}
   isna(data)
   # {'score': [False, True, True, False]}

   fillna(data, method="ffill", limit=1)
   # {'score': [10, 10, None, 20]}

   dropna(data, remaining=True)
   # [0, 3]

With ``remaining=True``, row operations return retained row indexes and column
operations return retained column names. For forward and backward filling,
``limit`` applies to each consecutive gap.

Joins
-----

The :mod:`tinytim.join` module provides inner, left, right, and full joins.
Join keys may be a column name or a sequence of names. Overlapping non-key
columns get ``_x`` and ``_y`` suffixes by default; pass ``suffixes`` to choose
different suffixes.

.. code-block:: python

   from tinytim.join import inner_join

   left = {"id": [1, 2], "value": ["old", "current"]}
   right = {"id": [2, 3], "value": ["new", "other"]}
   inner_join(left, right, "id")
   # {'id': [2], 'value_x': ['current'], 'value_y': ['new']}

   left = {"account": [10, 10], "year": [2025, 2026], "amount": [100, 120]}
   right = {"account": [10, 10], "year": [2025, 2026], "amount": [95, 125]}
   inner_join(left, right, ["account", "year"], suffixes=("_left", "_right"))

More examples
-------------

Runnable notebooks are available in the repository's
`examples directory <https://github.com/eddiethedean/tinytim/tree/main/examples>`_.
