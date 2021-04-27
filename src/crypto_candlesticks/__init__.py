# -*- coding: utf-8 -*-
"""The Crypto candlesticks project."""
try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import (  # type: ignore
        PackageNotFoundError,
        version,
    )


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = 'unknown'

from crypto_candlesticks import exchanges, symbols
