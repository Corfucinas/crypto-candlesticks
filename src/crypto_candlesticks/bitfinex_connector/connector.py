# -*- coding: utf-8 -*-
"""Main class for the Bitfinex exchange."""
from typing import List, TypeVar

import requests
from requests.exceptions import ConnectionError
from retry import retry

Api = TypeVar('Api', bound='Connector')


class Connector(object):
    """Main class for the Bitfinex exchange."""

    __slots__ = (
        '_end_point_v2',
        '_end_point_v1',
    )

    def __init__(self: Api) -> None:
        """Connector init."""
        self._end_point_v2 = 'https://api.bitfinex.com/v2/'
        self._end_point_v1 = 'https://api.bitfinex.com/v1/'

    def __repr__(self: Api) -> str:
        """Connector repr."""
        return 'Bitfinex connector class'

    @retry(ConnectionError, jitter=(0.1, 1))  # type: ignore
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
            '{}/candles/trade:{}:t{}/hist?limit={}&start={}&end={}&sort=-1'.format(
                self._end_point_v2,
                time_interval,
                ticker,
                10000,  # max allowed by Bitfinex
                start_time,
                end_time,
            ),
        ).json()

    @retry(ConnectionError, jitter=(0.1, 1))  # type: ignore
    def get_symbols(self: Api) -> List[str]:
        """Calls the exchange and gets all current tickers.

        Returns:
            List[str]: All available tickers.

        """
        return requests.get('{}/symbols'.format(self._end_point_v1)).json()
