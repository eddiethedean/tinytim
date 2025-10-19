# Contributing to TinyTim

Thank you for your interest in contributing to TinyTim! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/tinytim.git
cd tinytim
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies**

```bash
pip install -e ".[dev]"
# Or
pip install -r requirements_dev.txt
```

4. **Install pre-commit hooks** (optional but recommended)

```bash
pip install pre-commit
pre-commit install
```

## Code Quality

We use several tools to maintain code quality:

- **Ruff** for linting and formatting
- **Mypy** for type checking
- **Pytest** for testing

### Running checks locally

```bash
# Format code
ruff format src tests

# Lint code
ruff check src tests

# Type check
mypy src

# Run tests
pytest

# Run tests with coverage
pytest --cov=tinytim
```

### Using tox

You can run all checks across multiple Python versions using tox:

```bash
# Run all environments
tox

# Run specific environment
tox -e py312
tox -e ruff
tox -e mypy
```

## Coding Standards

1. **Python version support**: TinyTim supports Python 3.8+. Ensure your code is compatible with all supported versions.

2. **Type hints**: All functions should have proper type hints. Use types from `typing` or `collections.abc` as needed.

3. **Docstrings**: All public functions should have clear docstrings following the NumPy docstring format.

4. **Pure Python**: TinyTim has zero dependencies (except for development tools). Do not add runtime dependencies.

5. **Line length**: Maximum line length is 160 characters (configured in ruff).

## Testing

- Write tests for all new features and bug fixes
- Tests should be placed in the `tests/` directory
- Use descriptive test names that explain what is being tested
- Aim for high test coverage

```bash
# Run specific test file
pytest tests/test_data.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_data.py::test_column_count
```

## Pull Request Process

1. **Create a feature branch**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Write clear, concise commit messages
   - Keep commits focused and atomic
   - Add tests for new functionality

3. **Run all checks**

```bash
ruff format src tests
ruff check src tests
mypy src
pytest
```

4. **Push your branch**

```bash
git push origin feature/your-feature-name
```

5. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all CI checks pass

## Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes were made and why
- **Tests**: Include tests for new features
- **Documentation**: Update README.md or docstrings if needed
- **Breaking changes**: Clearly mark any breaking changes

## Reporting Issues

When reporting issues, please include:

- Python version
- TinyTim version
- Operating system
- Minimal code example that reproduces the issue
- Expected behavior vs actual behavior
- Error messages or stack traces

## Code Review

All contributions go through code review. Reviewers will check for:

- Code quality and style
- Test coverage
- Documentation
- Compatibility with supported Python versions
- Adherence to project philosophy (zero dependencies, pure Python)

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Contact the maintainer at odosmatthews@gmail.com

Thank you for contributing to TinyTim! 🎉

