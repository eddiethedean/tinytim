# TinyTim

A pure Python package for processing tabular data stored in dictionaries.

[![PyPI Latest Release](https://img.shields.io/pypi/v/tinytim.svg)](https://pypi.org/project/tinytim/)
![Tests](https://github.com/eddiethedean/tinytim/actions/workflows/tests.yml/badge.svg)
[![Python Version](https://img.shields.io/pypi/pyversions/tinytim.svg)](https://pypi.org/project/tinytim/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

TinyTim is a lightweight alternative to Pandas for processing tabular data. It's perfect for when you want to work with structured data but don't want to install Pandas and its many dependencies. TinyTim has **zero dependencies** outside of Python's standard library.

Data is stored in a simple dictionary format: `{column_name: column_values}`, making it easy to understand and work with.

## Features

- **Zero dependencies** - Pure Python implementation
- **Lightweight** - Minimal footprint, fast installation
- **Familiar API** - Intuitive functions for data manipulation
- **Type hints** - Full type annotations for better IDE support
- **Well tested** - Comprehensive test suite

## Installation

```bash
pip install tinytim
```

## Requirements

- Python >= 3.8

## Quick Start

### Basic Data Operations

```python
from tinytim.data import column_count, row_count, shape, head, tail

# Data is stored as {column_name: column_values}
data = {'x': [1, 2, 3, 4], 'y': [10, 20, 30, 40]}

# Get basic information
column_count(data)
# 2

row_count(data)
# 4

shape(data)
# (4, 2)

# Preview data
head(data, 2)
# {'x': [1, 2], 'y': [10, 20]}

tail(data, 2)
# {'x': [3, 4], 'y': [30, 40]}
```

### Working with Rows

```python
from tinytim.rows import row_dict, iterrows, row_dicts_to_data

data = {'x': [1, 2, 3], 'y': [6, 7, 8]}

# Get a single row
row_dict(data, 1)
# {'x': 2, 'y': 7}

# Iterate over rows
for index, row in iterrows(data):
    print(f"Row {index}: {row}")
# Row 0: {'x': 1, 'y': 6}
# Row 1: {'x': 2, 'y': 7}
# Row 2: {'x': 3, 'y': 8}

# Convert row dictionaries to data
rows = [{'x': 1, 'y': 20}, {'x': 2, 'y': 21}, {'x': 3, 'y': 22}]
result = row_dicts_to_data(rows)
# {'x': [1, 2, 3], 'y': [20, 21, 22]}
```

### Working with Columns

```python
from tinytim.edit import add_to_column, multiply_column

data = {'x': [1, 2, 3, 4], 'y': [5, 6, 7, 8]}

# Add to a column
result = add_to_column(data, 'x', 10)
# {'x': [11, 12, 13, 14], 'y': [5, 6, 7, 8]}

# Multiply a column
result = multiply_column(data, 'x', 2)
# {'x': [2, 4, 6, 8], 'y': [5, 6, 7, 8]}

# Column-wise operations with sequences
result = add_to_column(data, 'x', [10, 20, 30, 40])
# {'x': [11, 22, 33, 44], 'y': [5, 6, 7, 8]}
```

### Filtering and Selection

```python
from tinytim.filter import filter_by_column_gt, filter_by_column_isin

data = {'x': [1, 2, 3, 4, 5], 'y': [10, 20, 30, 40, 50]}

# Filter rows where column value is greater than threshold
filtered = filter_by_column_gt(data, 'x', 2)
# {'x': [3, 4, 5], 'y': [30, 40, 50]}

# Filter rows where column value is in a list
filtered = filter_by_column_isin(data, 'x', [1, 3, 5])
# {'x': [1, 3, 5], 'y': [10, 30, 50]}
```

### Handling Missing Values

```python
from tinytim.na import isna, dropna, fillna

data = {'x': [1, None, 3], 'y': [10, 20, None]}

# Check for missing values
isna(data)
# {'x': [False, True, False], 'y': [False, False, True]}

# Drop rows with missing values
dropna(data)
# {'x': [1], 'y': [10]}

# Fill missing values
fillna(data, 0)
# {'x': [1, 0, 3], 'y': [10, 20, 0]}

# Forward fill
data2 = {'x': [None, 2, None, 4], 'y': [10, None, None, 40]}
fillna(data2, method='ffill')
# {'x': [None, 2, 2, 4], 'y': [10, 10, 10, 40]}
```

### Grouping and Aggregation

```python
from tinytim.group import groupby, sum_groups

data = {'category': ['A', 'B', 'A', 'B'], 'value': [1, 2, 3, 4]}

# Group by column
groups = groupby(data, 'category')
# [('A', {'category': ['A', 'A'], 'value': [1, 3]}),
#  ('B', {'category': ['B', 'B'], 'value': [2, 4]})]

# Sum grouped data
labels, sums = sum_groups(groups)
# labels: ['A', 'B']
# sums: {'value': [4, 6]}
```

### Joining Data

```python
from tinytim.join import inner_join, left_join

left = {'id': [1, 2, 3], 'value': ['a', 'b', 'c']}
right = {'id': [2, 3, 4], 'score': [10, 20, 30]}

# Inner join on 'id' column
result = inner_join(left, right, 'id')
# {'id': [2, 3], 'value': ['b', 'c'], 'score': [10, 20]}

# Left join keeps all rows from left table
result = left_join(left, right, 'id')
# {'id': [1, 2, 3], 'value': ['a', 'b', 'c'], 'score': [None, 10, 20]}
```

## More Examples

### Editing Data

```python
from tinytim.edit import edit_row_items, drop_row, drop_column

data = {'name': ['Alice', 'Bob', 'Charlie'], 
        'age': [25, 30, 35], 
        'city': ['NYC', 'LA', 'SF']}

# Edit specific row values
result = edit_row_items(data, 1, {'age': 31, 'city': 'Seattle'})
# {'name': ['Alice', 'Bob', 'Charlie'], 
#  'age': [25, 31, 35], 
#  'city': ['NYC', 'Seattle', 'SF']}

# Drop a row
result = drop_row(data, 0)
# {'name': ['Bob', 'Charlie'], 'age': [30, 35], 'city': ['LA', 'SF']}

# Drop a column
result = drop_column(data, 'city')
# {'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]}
```

### Inserting Data

```python
from tinytim.insert import insert_row, insert_rows

data = {'x': [1, 2], 'y': [10, 20]}

# Insert a single row
result = insert_row(data, {'x': 3, 'y': 30})
# {'x': [1, 2, 3], 'y': [10, 20, 30]}

# Insert multiple rows
rows = [{'x': 4, 'y': 40}, {'x': 5, 'y': 50}]
result = insert_rows(data, rows)
# {'x': [1, 2, 4, 5], 'y': [10, 20, 40, 50]}
```

### Advanced Filtering

```python
from tinytim.filter import (
    filter_by_column_eq,
    filter_by_column_ne, 
    filter_by_column_le,
    sample
)

data = {'product': ['A', 'B', 'A', 'C', 'B'], 
        'price': [10, 20, 15, 30, 25]}

# Filter by equality
result = filter_by_column_eq(data, 'product', 'A')
# {'product': ['A', 'A'], 'price': [10, 15]}

# Filter by inequality
result = filter_by_column_ne(data, 'product', 'A')
# {'product': ['B', 'C', 'B'], 'price': [20, 30, 25]}

# Filter by less than or equal
result = filter_by_column_le(data, 'price', 20)
# {'product': ['A', 'B', 'A'], 'price': [10, 20, 15]}

# Random sample
result = sample(data, 2, random_state=42)
# Returns 2 random rows (deterministic with random_state)
```

### Copying Data

```python
from tinytim.copy import copy_table, deepcopy_table

data = {'x': [1, 2, 3], 'y': [[10], [20], [30]]}

# Shallow copy (copies dict and lists)
copy1 = copy_table(data)

# Deep copy (copies everything recursively)
copy2 = deepcopy_table(data)
copy2['y'][0][0] = 999
# Original data unchanged: data['y'][0][0] == 10
```

## Development

### Setting up a development environment

```bash
# Clone the repository
git clone https://github.com/eddiethedean/tinytim.git
cd tinytim

# Install development dependencies
pip install -e ".[dev]"

# Or use the requirements file
pip install -r requirements_dev.txt
```

### Running Tests

```bash
# Run tests with pytest
pytest

# Run tests with coverage
pytest --cov=tinytim

# Run tests across multiple Python versions
tox
```

### Linting and Type Checking

```bash
# Lint with ruff
ruff check src tests

# Format code with ruff
ruff format src tests

# Type check with mypy
mypy src
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Examples

See the [examples](https://github.com/eddiethedean/tinytim/tree/main/examples) directory for Jupyter notebooks demonstrating various features:

- [data.ipynb](https://github.com/eddiethedean/tinytim/blob/main/examples/data.ipynb) - Basic data operations
- [rows.ipynb](https://github.com/eddiethedean/tinytim/blob/main/examples/rows.ipynb) - Working with rows
- [columns.ipynb](https://github.com/eddiethedean/tinytim/blob/main/examples/columns.ipynb) - Working with columns
- [join.ipynb](https://github.com/eddiethedean/tinytim/blob/main/examples/join.ipynb) - Joining datasets
- [group.ipynb](https://github.com/eddiethedean/tinytim/blob/main/examples/group.ipynb) - Grouping and aggregation
- [fillna.ipynb](https://github.com/eddiethedean/tinytim/blob/main/examples/fillna.ipynb) - Handling missing values

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**Odos Matthews** - [odosmatthews@gmail.com](mailto:odosmatthews@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/eddiethedean/tinytim/blob/main/LICENSE.md) file for details.

## Why TinyTim?

TinyTim is ideal for:

- **Embedded systems** or environments with limited resources
- **Lambda functions** or serverless applications where package size matters
- **Learning** data manipulation concepts without the complexity of Pandas
- **Scripts** where you need basic data operations without heavy dependencies
- **Distribution** of tools where you want to minimize user installation burden