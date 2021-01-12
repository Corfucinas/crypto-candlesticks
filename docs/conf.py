# -*- coding: utf-8 -*-
"""Sphinx configuration."""
from datetime import datetime

project = 'Crypto Candlesticks'
author = 'Pedro Torres'
copyright = f'{datetime.now().year}, {author}'
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
]
html_static_path = ['_static']
