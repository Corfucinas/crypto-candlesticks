# -*- coding: utf-8 -*-
"""Command-line program to download cryptocurrencies OHLCV.

Released under the GPL-3.0-or-later license
"""


# built-in
from importlib.metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)  # noqa: F401
except PackageNotFoundError:
    __version__ = 'unknown'

__author__ = 'Pedro Torres <corfucinas@protonmail.com>'  # noqa: WPS410


# project
from crypto_candlesticks import exchanges, symbols  # noqa: F401


__all__ = ['symbols', 'exchanges']  # noqa: WPS410
