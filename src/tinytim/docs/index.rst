TinyTim documentation
=====================

TinyTim is a small, pure-Python toolkit for working with tables represented as
mappings of column names to sequences. It has no runtime dependencies and
supports Python 3.11 and newer.

Install TinyTim with pip:

.. code-block:: console

   python -m pip install tinytim

A table is an ordinary mapping. Keep all of its columns the same length:

.. code-block:: python

   data = {"name": ["Ada", "Lin"], "score": [95, 88]}

The user guide covers common operations. The API reference lists the package's
public modules and functions.

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   code
   modules

TinyTim is developed on `GitHub <https://github.com/eddiethedean/tinytim>`_.
