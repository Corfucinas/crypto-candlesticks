# -*- coding: utf-8 -*-
"""Command-line interface for Crypto Candlesticks."""

import datetime
import time

import click

from crypto_candlesticks.get_data import get_data
from crypto_candlesticks.validate_symbol import validate

click.secho('Welcome, what data do you wish to download?', fg='green')


@click.command()
@click.option(
    '-s',
    '--symbol',
    type=str,
    prompt='Cryptocurrency symbol to download (ie. BTC, ETH, LTC)',
    help='Cryptocurrency ticker symbol',
)
@click.option(
    '-b',
    '--base_currency',
    type=click.Choice((validate), case_sensitive=False),
    prompt='Base pair',
    help='Cryptocurrency base trading pair',
)
@click.option(
    '-i',
    '--interval',
    type=click.Choice(
        [
            '1m',
            '5m',
            '15m',
            '30m',
            '1h',
            '3h',
            '6h',
            '12h',
            '1D',
            '7D',
            '14D',
            '1M',
        ],
    ),
    prompt='Interval to download the candlestick data',
    help='Interval that will be used to download the data.',
)
@click.option(
    '-sd',
    '--start_date',
    type=click.DateTime(),
    prompt='Date to start downloading the data (ie. YYYY-MM-DD)',
    help='YYYY, MM, DD from which the candlestick data will start.',
)
@click.option(
    '-ed',
    '--end_date',
    type=click.DateTime(),
    prompt='Date up to the data will be downloaded (ie. YYYY-MM-DD)',
    help='YYYY, MM, DD up to which the candlestick data will be downloaded.',
)
def main(
    symbol: str,
    base_currency: str,
    interval: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> None:
    """Download cryptoccurency candlestick data from Bitfinex.

    If the data is obtained successfully, it will be converted to a .csv,
    sqlite3 database, and a pickle file.

    Arguments:
        symbol (str): Cryptocurrency ticker.
        base_currency (str): Base pair.
        start_date (str): Beginning date.
        end_date (str): Ending date.
        interval (str): Ticker Interval.
    """
    symbol = symbol.upper()
    base_currency = base_currency.upper()
    time_start = (
        time.mktime(
            datetime.datetime(
                start_date.year, start_date.month, start_date.day, 0, 0,
            ).timetuple(),
        )
        * 1000
    )
    time_stop = (
        time.mktime(
            datetime.datetime(
                end_date.year, end_date.month, end_date.day, 0, 0,
            ).timetuple(),
        )
        * 1000
    )
    get_data(
        symbol, base_currency, time_start, time_stop, interval,
    )
