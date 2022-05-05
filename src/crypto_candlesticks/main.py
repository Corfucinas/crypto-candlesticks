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

"""Command-line interface for Crypto Candlesticks."""

# built-in
import time
from datetime import datetime

# external
import click

# project
from crypto_candlesticks.get_data import download_data
from crypto_candlesticks.symbols.quote_currencies import quote_currencies_list
from crypto_candlesticks.symbols.time_intervals import time_intervals_list


def time_clamp() -> int:
    """Get current time in milliseconds.

    Returns:
        int: Current time in milliseconds
    """
    return int(round(time.time() * 1000))


def fix_time() -> float:
    """Ensure the end_data is not after than today's date.

    Returns:
        float: Todays date in milliseconds
    """
    return (
        time.mktime(
            datetime(
                datetime.now().year,
                datetime.now().month,
                datetime.now().day,
                8,
                0,
            ).timetuple()
        )
        * 1000
    )


def make_time(date: datetime) -> float:
    """Make time in milliseconds.

    Args:
        date (datetime): Datetime object to convert to milliseconds

    Returns:
        float: Datetime be converted to milliseconds
    """
    return (
        time.mktime(
            datetime(date.year, date.month, date.day, 8, 0).timetuple(),
        )
        * 1000
    )


def main() -> None:
    """Print to console the welcome message."""
    click.secho('Welcome, what data do you wish to download?\n', fg='green')
    collect_arguments()


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
    type=click.Choice(quote_currencies_list, case_sensitive=False),
    prompt='Base pair',
    help='Cryptocurrency base trading pair',
)
@click.option(
    '-i',
    '--interval',
    type=click.Choice(time_intervals_list, case_sensitive=True),
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
def collect_arguments(  # noqa: WPS216
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
        interval (str): Ticker Interval.
        start_date (datetime): Beginning date.
        end_date (datetime): Ending date.
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

    download_data(
        symbol.upper(),
        base_currency.upper(),
        time_start,
        time_stop,
        interval,
    )


if __name__ == '__main__':
    main()
