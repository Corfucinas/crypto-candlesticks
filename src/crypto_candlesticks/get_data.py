# -*- coding: utf-8 -*-
"""The Crypto candlesticks engine."""

# built-in
import pickle  # noqa: S40  # nosec
import sys
import time
from typing import Annotated, Union

# external
import click
import pandas as pd
from rich.live import Live

# project
from crypto_candlesticks.database import SqlDatabase
from crypto_candlesticks.exchanges.bitfinex import Bitfinex
from crypto_candlesticks.text_console import setup_table, write_to_console


Time = Annotated[float, 'Datetime in Unix time']
Interval = Annotated[str, 'Time intervals allowed by the exchange']

_RATE_LIMIT = 1.85
_STEP_SIZE = 86400000


Candles = list[list[list[Union[int, float]]]]


def get_candles(  # noqa: WPS210
    ticker: str,
    start_time: Time,
    end_time: Time,
    interval: Interval,
    step_size: int = _STEP_SIZE,
) -> Candles:
    """Call the exchange for the data and extends it into a list.

    Args:
        ticker (str): Ticker to download the data.
        start_time (Time): Time in ms on which the data will start.
        end_time (Time): Time in ms on which the data will finish.
        interval (Interval): Period downloaded.
        step_size (int): The size step for each call. Defaults to _STEP_SIZE.

    Returns:
        Candles: A list of floats containing OHLC

    """
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
    with Live(
        vertical_overflow='ellipsis',
        auto_refresh=False,
    ) as live:
        while start_time <= end_time:
            period = start_time + step_size
            max_candles_allowed = 10000
            candlestick = exchange.get_candles(
                ticker=ticker,
                time_interval=interval,
                history_limit=max_candles_allowed,
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
            time.sleep(_RATE_LIMIT)

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

    df = pd.DataFrame(
        candle_data,
        columns=['timestamp', 'open', 'close', 'high', 'low', 'volume'],
    )
    df.drop_duplicates(inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index(
        'timestamp',
        inplace=True,
    )
    df.sort_index(inplace=True)
    df['ticker'] = f'{symbol}/{base_currency}'
    df['date'] = pd.to_datetime(df.index, format='%Y:%M:%D').date
    df['time'] = pd.to_datetime(df.index, format='%Y:%M:%D').time
    return df


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
    time_start: Time,
    time_stop: Time,
    interval: Interval,
) -> None:
    """Handle the OHLC response and conversion.

    Args:
        symbol (str): [description]
        base_currency (str): [description]
        time_start (Time): [description]
        time_stop (Time): [description]
        interval (Interval): [description]
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

    click.secho(
        'Data download completed! 🚀',
        fg='green',
    )
    click.secho(
        'Processing data...',
        fg='yellow',
    )
    output = f'{ticker}-{interval}'
    df = write_data_to_sqlite(
        symbol,
        base_currency,
        interval,
        ticker,
        candle_stick_data,
        output,
    )
    write_data_to_excel(output, df)


def write_data_to_excel(output: str, df: pd.DataFrame) -> None:
    """Write data to excel file.

    Args:
        output (str): [description]
        df (pd.DataFrame): [description]
    """
    click.secho(
        'Writing to Excel...',
        fg='yellow',
    )
    df.to_csv(
        path_or_buf=output + str(f'{time.time()}.csv'),
        sep=',',
        header=True,
        index=False,
    )
    click.secho(
        'Writing to Excel completed! 🚀🚀🚀',
        fg='green',
    )


def write_data_to_sqlite(  # noqa: WPS211
    symbol: str,
    base_currency: str,
    interval: Interval,
    ticker: Interval,
    candle_stick_data: Candles,
    output: str,
) -> pd.DataFrame:
    """Write data to sqlite database.

    Args:
        symbol (str): [description]
        base_currency (str): [description]
        interval (Interval): [description]
        ticker (Interval): [description]
        candle_stick_data (Candles): [description]
        output (str): [description]

    Returns:
        pd.DataFrame: [description]
    """
    with open(f'{output}.p', 'wb') as create_pickle_file:
        pickle.dump(
            candle_stick_data,
            create_pickle_file,
        )
    df = convert_data(symbol, base_currency, candle_stick_data)
    SqlDatabase(f'{output}.sqlite3').insert_candlesticks(
        candle_stick_data,
        ticker,
        interval,
    )
    click.secho(
        'Writing to database completed! 🚀🚀',
        fg='green',
    )

    return df


def print_exit_error_message(time_start: Time, time_stop: Time) -> None:
    """Print error message if data could not be downloaded.

    Args:
        time_start (Time): [description]
        time_stop (Time): [description]
    """
    time_start = pd.to_datetime(time_start, unit='ms')
    time_stop = pd.to_datetime(time_stop, unit='ms')
    error_message: str = f"""\n
        Data could not be downloaded
        The data period is {time_start} until {time_stop}
        Confirm that the time period is correct and the exchange is online"""

    click.secho(error_message, fg='red')

    sys.exit(1)
