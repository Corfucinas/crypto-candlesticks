# -*- coding: utf-8 -*-
"""Test quote currency is listed."""
import requests

from crypto_candlesticks.symbols.quote_currency import quote_currency


def test_quote_currency() -> None:
    """Test is quote currency is listed."""
    bitfinex_endpoint = 'https://api.bitfinex.com/v1/symbols'
    symbols = requests.get(bitfinex_endpoint)
    try:
        assert symbols.status_code == 200
    except AssertionError:
        print('Endpoint is offline')
        raise
    for symbol in quote_currency:
        try:
            assert symbol.lower() in symbols.text
        except AssertionError as error:
            print(f'Symbol is: {symbol}')
            print(f'Quote currency is: {quote_currency}')
            print(f'test failed: {error}')
            raise
