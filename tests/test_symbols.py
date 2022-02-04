# -*- coding: utf-8 -*-
"""Test quote currency is listed."""
# external
import requests

# project
from crypto_candlesticks.symbols.quote_currencies import quote_currencies_list


def test_quote_currency() -> None:
    """Test is quote currency is listed."""
    bitfinex_endpoint = 'https://api.bitfinex.com/v1/symbols'
    symbols = requests.get(bitfinex_endpoint)
    try:
        assert symbols.status_code == 200
    except AssertionError:
        print('Endpoint is offline')
        raise
    for symbol in quote_currencies_list:
        try:
            assert symbol.lower() in symbols.text
        except AssertionError as error:
            print(f'Symbol is: {symbol}')
            print(f'Quote currency is: {quote_currencies_list}')
            print(f'test failed: {error}')
            raise
