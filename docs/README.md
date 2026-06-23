# Sphinx Documentation for micropython-dgus

This directory contains the Sphinx documentation configuration for the
micropython-dgus library.

## Building Documentation Locally

### Prerequisites

```bash
pip install -r requirements.txt
```

### Build HTML Documentation

```bash
cd docs
make html
```

The generated documentation will be in `build/html/index.html`.

### Clean Build

```bash
make clean
```

## GitHub Pages Deployment

No deployment workflow is documented here.

## Configuration

- `source/conf.py` - Sphinx configuration with Napoleon extension for parsing Google and NumPy style docstrings
- `source/index.rst` - Main documentation index page
- `source/api/index.rst` - API reference entry point (autodoc/autosummary from Python docstrings)

## Docstring Format

The library uses **reStructuredText** format for docstrings, which Sphinx parses natively:

```python
def example_function(param1, param2):
    """Brief description of the function.

    Longer description with more details.

    :param param1: Description of first parameter
    :param param2: Description of second parameter
    :returns: Description of return value
    :rtype: return_type
    :raises ValueError: When something goes wrong
    """
```

Sphinx with Napoleon also supports Google-style docstrings for backwards compatibility.
