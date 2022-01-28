# -*- coding: utf-8 -*-
"""The Crypto candlesticks project."""

# built-in
from importlib.metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)  # noqa: F401
except PackageNotFoundError:
    __version__ = 'unknown'

# project
from crypto_candlesticks import exchanges, symbols  # noqa: F401
