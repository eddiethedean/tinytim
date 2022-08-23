from curses import tigetflag
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="tinytim",
    version="0.10.1",
    description="Pure Python data table functions.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/eddiethedean/tinytim",
    author="Odos Matthews",
    author_email="odosmatthews@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=['tinytim'],
    py_modules=['tinytim.columns', 'tinytim.copy', 'tinytim.edit'
                'tinytim.features', 'tinytim.filter', 'tinytim.group',
                'tinytim.rows', 'tinytim.utils', 'tinytim.validate'],
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[]
)