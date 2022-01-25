"""Sphinx configuration."""
from datetime import datetime

project = 'Crypto Candlesticks'
author = 'Pedro Torres'
year = datetime.now().year
copyright = f'{year}, {author}'
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
]
html_theme = 'furo'
html_static_path = ['_static']
