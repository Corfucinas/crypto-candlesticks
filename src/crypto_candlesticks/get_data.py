# -*- coding: utf-8 -*-
"""The Crypto candlesticks engine."""

import pickle
import time
from typing import List

import click
import pandas as pd
from tqdm import tqdm

from crypto_candlesticks.bitfinex_connector.connector import Connector
from crypto_candlesticks.database import SqlDatabase

_RATE_LIMIT = 1.1
_BIN_LIMIT = 1000
_MAX_CALL_PER_MIN = 60
_STEP_SIZE = _BIN_LIMIT * _MAX_CALL_PER_MIN * _BIN_LIMIT


def get_candles(
    ticker: str,
    start_time: float,
    end_time: float,
    interval: str,
    limit: int = _BIN_LIMIT,
    step_size: int = _STEP_SIZE,
) -> List[float]:
    """Calls the exchange for the data and extends it into a list.

    Args:
        ticker (str): Ticker to download the data.
        start_time (float): Time in ms on which the data will start.
        end_time (float): Time in ms on which the data will finish.
        interval (str): Period downloaded.
        limit (int): Limits the size step. Defaults to _BIN_LIMIT.
        step_size (int): The size step for each call. Defaults to _STEP_SIZE.

    Returns:
        List[float]: A list of floats containing OHLC
    """
    candle_data = []
    if validate_symbol(ticker):
        click.echo(f'Collecting {ticker} data for {interval}')
        with tqdm(total=int(100)) as pbar:
            pbar.set_description('Downloading and converting the data')
            while start_time <= end_time:
                period = start_time + step_size
                candlestick = Connector().get_candles(
                    ticker=ticker,
                    time_interval=interval,
                    limit=limit,
                    start_time=start_time,
                    end_time=period,
                )
                candle_data.extend(candlestick)
                start_time = period
                pbar.update(int(end_time / start_time))
                time.sleep(_RATE_LIMIT)
    else:
        click.secho(
            "Data could not be downloaded ❌, check '{}' is listed on Bitfinex".format(
                ticker,
            ),
            fg='red',
        )
    return candle_data


def convert_data(
    symbol: str, base_currency: str, candle_data: List[float],
) -> pd.DataFrame:
    """Process results from API into data analysis format.

    Args:
        symbol (str): Symbol that is downloaded
        base_currency (str): Base pair that is traded
        candle_data (List[float]): Candlestick OHLC data

    Returns:
        pd.DataFrame: Standard DataFrame object
    """
    if not candle_data:
        click.echo('Data could not be downloaded ❌, please try again')

    df = pd.DataFrame(
        candle_data,
        columns=['timestamp', 'open', 'close', 'high', 'low', 'volume'],
    )
    df.drop_duplicates(inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index(
        'timestamp', inplace=True,
    )
    df.sort_index(inplace=True)
    df['ticker'] = symbol + '{}'.format('/') + base_currency
    df['date'] = pd.to_datetime(df.index, format='%Y:%M:%D').date
    df['time'] = pd.to_datetime(df.index, format='%Y:%M:%D').time
    return df


def validate_symbol(symbol: str) -> bool:  # type: ignore
    """Returns True if the symbol is active on Bitfinex.

    Args:
        symbol (str): The symbol to validate

    Returns:
        bool: Returns True if the symbol is active, else False
    """
    all_symbols = Connector().get_symbols()
    for symbols in all_symbols:
        if symbol.lower() in symbols:
            return True


def get_data(
    symbol: str,
    base_currency: str,
    time_start: float,
    time_stop: float,
    interval: str,
) -> None:
    """Function for handling the OHLC response and conversion."""
    ticker = symbol + base_currency
    candle_stick_data = get_candles(
        ticker=ticker,
        start_time=time_start,
        end_time=time_stop,
        interval=interval,
    )
    if candle_stick_data:
        output = ticker + '{}'.format('-') + interval
        with open(output + '{}'.format('.p'), 'wb') as create_file:
            pickle.dump(
                candle_stick_data, create_file,
            )
        with open(output + '{}'.format('.p'), 'rb') as load_data:
            candle_stick_data = pickle.load(load_data)
        df = convert_data(symbol, base_currency, candle_stick_data)
        SqlDatabase(output + '{}'.format('.sqlite3')).insert_candlesticks(
            candle_stick_data, ticker, interval,
        )
        df.to_csv(
            path_or_buf=output + str(time.time()) + '{}'.format('.csv'),
            sep=',',
            header=True,
            index=False,
        )
        click.secho(
            'Data processing completed 🚀🚀🚀', fg='green',
        )
    else:
        click.secho(
            'Confirm the inputs are correct and the exchange is online ✍️',
            fg='yellow',
        )
