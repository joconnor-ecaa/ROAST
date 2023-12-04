"""Sphinx configuration."""
project = "Roastmaster"
author = "Joe O'Connor"
copyright = "2023, Joe O'Connor"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
