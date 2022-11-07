import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="tinytim",
    version="1.9.1",
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
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['dictanykey>=0.0.2', 'hasattrs>=0.0.2']
)