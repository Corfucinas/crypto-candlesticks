# -*- coding: utf-8 -*-

#  Copyright (C) 2021 Pedro Torres

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Main class for the Bitfinex exchange."""


# built-in
from typing import List

# external
import requests
from retry import retry


class Bitfinex(object):  # noqa: R0205
    """Main class for the Bitfinex exchange."""

    __slots__ = ('_end_point_v2', '_end_point_v1')

    def __init__(self) -> None:
        """Bitfinex init."""
        self._end_point_v2 = 'https://api.bitfinex.com/v2/'
        self._end_point_v1 = 'https://api.bitfinex.com/v1/'

    def __repr__(self) -> str:
        """Bitfinex repr.

        Returns:
            str: Class representation
        """
        return 'Bitfinex exchange class'

    @retry(ConnectionError, jitter=(0.1, 1))
    def get_candles(  # noqa: WPS211 R0913
        self,
        ticker: str,
        history_limit: int,
        time_interval: str,
        start_time: float,
        end_time: float,
    ) -> List[float]:
        """Download the candlestick data for the given period.

        Args:
            ticker (str): Cryptocurrency pair
            history_limit (int): Candlesticks to download, varies per exchange
            time_interval (str): Interval of the data
            start_time (float): Time in ms on which the data will start
            end_time (float): Time in ms on which the data will finish

        Returns:
            List[float]: Returns a List of candle data which can be parsed

        """
        url = f'{self._end_point_v2}/candles/trade:{time_interval}:t{ticker}/hist?limit={history_limit}&start={start_time}&end={end_time}&sort=-1'  # noqa: E501, WPS221, C0301

        return requests.get(url).json()

    @retry(ConnectionError, jitter=(0.1, 1))
    def get_symbols(self) -> List[str]:
        """Call the exchange and gets all current tickers.

        Returns:
            List[str]: All available tickers.

        """
        return requests.get(f'{self._end_point_v1}/symbols').json()
