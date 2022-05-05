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

"""The Crypto candlesticks engine."""

# built-in
import pickle  # noqa: S403  # nosec
import sys
from time import sleep, time
from typing import List, Union

# external
import click
import pandas as pd
from rich.live import Live

# project
from crypto_candlesticks.database import SqlDatabase
from crypto_candlesticks.exchanges.bitfinex import Bitfinex
from crypto_candlesticks.text_console import setup_table, write_to_console


Candles = List[List[List[Union[int, float]]]]


def get_candles(  # noqa: WPS210
    ticker: str,
    start_time: float,
    end_time: float,
    interval: str,
    step_size: int = 86400000,
) -> Candles:
    """Call the exchange for the data and extends it into a list.

    Args:
        ticker (str): Ticker to download the data.
        start_time (float): Time in ms on which the data will start.
        end_time (float): Time in ms on which the data will finish.
        interval (str): Period downloaded.
        step_size (int): The size step for each call. Defaults to _STEP_SIZE.

    Returns:
        Candles: A list of floats containing OHLC

    """
    rate_limit = 1.85

    candle_data: Candles = []
    if not validate_symbol(ticker.lower()):
        click.secho(
            f"Cannot download ❌, check '{ticker}' is listed on Bitfinex",
            fg='red',
        )
        sys.exit(1)

    click.secho(
        f'Downloading {ticker} data for {interval} interval...',
        fg='yellow',
    )
    exchange = Bitfinex()
    with Live(vertical_overflow='ellipsis', auto_refresh=False) as live:
        while start_time <= end_time:
            period = start_time + step_size
            max_candles = 10000
            candlestick = exchange.get_candles(
                ticker=ticker,
                time_interval=interval,
                history_limit=max_candles,
                start_time=start_time,
                end_time=period,
            )
            candle_data.extend(candlestick)
            write_to_console(
                ticker,
                interval,
                candlestick,
                live,
                setup_table(),
            )
            live.refresh()
            start_time = period
            sleep(rate_limit)

    return candle_data


def convert_data(
    symbol: str,
    base_currency: str,
    candle_data: Candles,
) -> pd.DataFrame:
    """Process results from API into data analysis format.

    Args:
        symbol (str): Symbol that is downloaded
        base_currency (str): Base pair that is traded
        candle_data (Candles): Candlestick OHLC data

    Returns:
        pd.DataFrame: Standard DataFrame object
    """
    if not candle_data:
        click.echo('Data could not be downloaded ❌, please try again')
        sys.exit(1)

    dataframe = pd.DataFrame(
        candle_data,
        columns=['timestamp', 'open', 'close', 'high', 'low', 'volume'],
    )
    dataframe.drop_duplicates(inplace=True)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit='ms')
    dataframe.set_index('timestamp', inplace=True)
    dataframe.sort_index(inplace=True)
    dataframe['ticker'] = f'{symbol}/{base_currency}'
    dataframe['date'] = pd.to_datetime(dataframe.index, format='%Y:%M:%D').date
    dataframe['time'] = pd.to_datetime(dataframe.index, format='%Y:%M:%D').time
    return dataframe


def validate_symbol(crypto_ticker: str) -> bool:
    """Return True if the symbol is active on Bitfinex.

    Args:
        crypto_ticker (str): The symbol to validate

    Returns:
        bool: Returns True if the symbol is active, else False

    """
    return crypto_ticker in Bitfinex().get_symbols()


def download_data(
    symbol: str,
    base_currency: str,
    time_start: float,
    time_stop: float,
    interval: str,
) -> None:
    """Handle the OHLC response and conversion.

    Args:
        symbol (str): Quote currency to download.
        base_currency (str): Base currency to download.
        time_start (float): Datetime in Unix time.
        time_stop (float): Datetime in Unix time.
        interval (str): Time intervals allowed by the exchange.
    """
    ticker = symbol + base_currency
    candle_stick_data = get_candles(
        ticker=ticker,
        start_time=time_start,
        end_time=time_stop,
        interval=interval,
    )
    if not candle_stick_data:
        print_exit_error_message(time_start, time_stop)

    click.secho('Data download completed! 🚀', fg='green')
    click.secho('Processing data...', fg='yellow')
    crypto_currency_pair = f'{ticker}-{interval}'
    dataframe = write_data_to_sqlite(
        symbol,
        base_currency,
        interval,
        ticker,
        candle_stick_data,
        crypto_currency_pair,
    )
    write_data_to_excel(crypto_currency_pair, dataframe)


def write_data_to_excel(
    crypto_currency_pair: str,
    dataframe: pd.DataFrame,
) -> None:
    """Write data to excel file.

    Args:
        crypto_currency_pair (str): Ticker pair downloaded.
        dataframe (pd.DataFrame): Dataframe containing the OHLCV data.
    """
    click.secho('Writing to Excel...', fg='yellow')
    dataframe.to_csv(
        path_or_buf=crypto_currency_pair + str(f'{time()}.csv'),
        sep=',',
        header=True,
        index=False,
    )
    click.secho('Writing to Excel completed! 🚀🚀🚀', fg='green')


def write_data_to_sqlite(  # noqa: WPS211 R0913
    symbol: str,
    base_currency: str,
    interval: str,
    ticker: str,
    candle_stick_data: Candles,
    output: str,
) -> pd.DataFrame:
    """Write data to sqlite database.

    Args:
        symbol (str): Symbol that is downloaded
        base_currency (str): Base pair that is traded
        interval (str): Time interval of the candles
        ticker (str): Cryptocurrency pair
        candle_stick_data (Candles): Candlestick OHLC data
        output (str): Cryptocurrency pair string

    Returns:
        pd.DataFrame: Pandas dataframe
    """
    with open(f'{output}.p', 'wb') as create_pickle_file:
        pickle.dump(candle_stick_data, create_pickle_file)
    dataframe = convert_data(symbol, base_currency, candle_stick_data)
    SqlDatabase(f'{output}.sqlite3').insert_candlesticks(
        candle_stick_data,
        ticker,
        interval,
    )
    click.secho('Writing to database completed! 🚀🚀', fg='green')

    return dataframe


def print_exit_error_message(time_start: float, time_stop: float) -> None:
    """Print error message if data could not be downloaded.

    Args:
        time_start (float): Datetime in Unix time.
        time_stop (float): Datetime in Unix time.
    """
    time_start = pd.to_datetime(time_start, unit='ms')
    time_stop = pd.to_datetime(time_stop, unit='ms')
    error_message: str = f"""\n
        Data could not be downloaded
        The data period is {time_start} until {time_stop}
        Confirm that the time period is correct and the exchange is online"""

    click.secho(error_message, fg='red')

    sys.exit(1)
