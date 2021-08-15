# -*- coding: utf-8 -*-
"""Command-line interface for Crypto Candlesticks."""

import time
from datetime import datetime

import click

from crypto_candlesticks.get_data import get_data
from crypto_candlesticks.symbols.intervals import intervals
from crypto_candlesticks.symbols.quote_currency import quote_currency

click.secho('Welcome, what data do you wish to download?', fg='green')


def time_clamp() -> int:
    """Get current time in milliseconds.

    Returns:
        int: Current time in milliseconds
    """
    return int(round(time.time() * 1000))


def fix_time() -> float:
    """Fix time to a specific period."""
    return (
        time.mktime(
            datetime(
                datetime.today().year,
                datetime.today().month,
                datetime.today().day,
                8,
                0,
            ).timetuple(),
        )
        * 1000
    )


def make_time(date: datetime) -> float:
    """Make time in milliseconds."""
    return (
        time.mktime(
            datetime(
                date.year,
                date.month,
                date.day,
                8,
                0,
            ).timetuple(),
        )
        * 1000
    )


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
    type=click.Choice(quote_currency, case_sensitive=False),
    prompt='Base pair',
    help='Cryptocurrency base trading pair',
)
@click.option(
    '-i',
    '--interval',
    type=click.Choice(intervals, case_sensitive=True),
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
    start_date: datetime,
    end_date: datetime,
) -> None:
    """Download cryptocurrency candlestick data from Bitfinex.

    If the data is obtained successfully, it will be converted to a .csv,
    sqlite3 database, and a pickle file.

    Args:
        symbol (str): Cryptocurrency ticker.
        base_currency (str): Base pair.
        interval (str): Beginning date.
        start_date (datetime): Ending date.
        end_date (datetime): Ticker Interval.
    """
    one_day: int = 86400000

    time_start: float = (
        make_time(start_date)
        if make_time(start_date) < time_clamp()
        else fix_time()
    )

    time_stop: float = (
        make_time(end_date)
        if make_time(end_date) < time_clamp()
        else fix_time() - one_day
    )

    get_data(
        symbol.upper(),
        base_currency.upper(),
        time_start,
        time_stop,
        interval,
    )


if __name__ == '__main__':
    main()
