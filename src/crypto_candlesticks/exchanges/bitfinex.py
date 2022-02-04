# -*- coding: utf-8 -*-
"""Main class for the Bitfinex exchange."""

# external
import requests
from requests.exceptions import ConnectionError
from retry import retry


class Bitfinex(object):
    """Main class for the Bitfinex exchange."""

    __slots__ = ('_end_point_v2', '_end_point_v1')

    def __init__(self) -> None:
        """Bitfinex init."""
        self._end_point_v2: str = 'https://api.bitfinex.com/v2/'
        self._end_point_v1: str = 'https://api.bitfinex.com/v1/'

    def __repr__(self) -> str:
        """Bitfinex repr.

        Returns:
            str: Class representation
        """
        return 'Bitfinex class'

    @retry(ConnectionError, jitter=(0.1, 1))
    def get_candles(
        self,
        ticker: str,
        history_limit: int,
        time_interval: str,
        start_time: float,
        end_time: float,
    ) -> list[float]:
        """Download the candlestick data for the given period.

        Args:
            ticker (str): Cryptocurrency pair
            history_limit (int): Candlesticks to download, varies per exchange
            time_interval (Interval): Interval of the data
            start_time (Time): Time in ms on which the data will start
            end_time (Time): Time in ms on which the data will finish

        Returns:
            list[float]: Returns a list of candle data which can be parsed

        """
        return requests.get(
            f'{self._end_point_v2}/candles/trade:{time_interval}:t{ticker}/hist?limit={history_limit}&start={start_time}&end={end_time}&sort=-1',
        ).json()

    @retry(ConnectionError, jitter=(0.1, 1))
    def get_symbols(self) -> list[str]:
        """Call the exchange and gets all current tickers.

        Returns:
            list[str]: All available tickers.

        """
        return requests.get(f'{self._end_point_v1}/symbols').json()
