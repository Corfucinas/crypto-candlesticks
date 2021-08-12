# -*- coding: utf-8 -*-
"""Main class for the Bitfinex exchange."""
from typing import List, TypeVar

import requests
from requests.exceptions import ConnectionError
from retry import retry

Api = TypeVar('Api', bound='Bitfinex')


class Bitfinex(object):
    """Main class for the Bitfinex exchange."""

    __slots__ = (
        '_end_point_v2',
        '_end_point_v1',
    )

    def __init__(self: Api) -> None:
        """Bitfinex init."""
        self._end_point_v2: str = 'https://api.bitfinex.com/v2/'
        self._end_point_v1: str = 'https://api.bitfinex.com/v1/'

    def __repr__(self: Api) -> str:
        """Bitfinex repr."""
        return 'Bitfinex class'

    @retry(ConnectionError, jitter=(0.1, 1))
    def get_candles(
        self: Api,
        ticker: str,
        time_interval: str,
        start_time: float,
        end_time: float,
    ) -> List[float]:
        """Downloads the candlestick data for the given period.

        Args:
            ticker (str): Cryptocurrency pair
            time_interval (str): Interval of the data
            start_time (float): Time in ms on which the data will start
            end_time (float): Time in ms on which the data will finish

        Returns:
            List[float]: Returns a list of candle data which can be parsed

        """
        return requests.get(
            f'{self._end_point_v2}/candles/trade:{time_interval}:t{ticker}/hist?limit={10000}&start={start_time}&end={end_time}&sort=-1',
        ).json()

    @retry(ConnectionError, jitter=(0.1, 1))
    def get_symbols(self: Api) -> List[str]:
        """Calls the exchange and gets all current tickers.

        Returns:
            List[str]: All available tickers.

        """
        return requests.get(f'{self._end_point_v1}/symbols').json()
