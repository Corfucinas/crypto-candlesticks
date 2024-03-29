# -*- coding: utf-8 -*-
"""Sphinx configuration."""


# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------

# built-in
from datetime import datetime


project = 'crypto-candlesticks'
year = datetime.now().year
author = 'Pedro Torres'
copyright = f'{year}, {author}'  # noqa: WPS305
numfig = True

# The full version, including alpha/beta/rc tags
release = '0.2.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinxext.opengraph',
    'sphinxcontrib.spelling',
    'sphinx_copybutton',
]
napoleon_use_param = True
spelling_warning = True
spelling_show_suggestions = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.


html_theme = 'furo'
html_theme_options = {'navigation_with_keys': True}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
