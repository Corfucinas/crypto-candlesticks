# -*- coding: utf-8 -*-
"""Command-line program to download cryptocurrencies OHLCV.

Released under the GPL-3.0-or-later license
"""


# built-in
try:
    # built-in
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import (  # type: ignore
        version,
        PackageNotFoundError,
    )  # noqa: WPS433 E501

# project
from crypto_candlesticks import exchanges, symbols  # noqa: F401


try:
    __version__ = version(__name__)  # noqa: F401
except PackageNotFoundError:
    __version__ = 'unknown'

__author__ = 'Pedro Torres <corfucinas@protonmail.com>'  # noqa: WPS410


__all__ = ('symbols', 'exchanges')  # noqa: WPS410
