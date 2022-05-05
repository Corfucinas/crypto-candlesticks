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


"""Display data in the CLI using Rich."""
# built-in
from typing import List, Union

# external
import pandas as pd
from pandas import Timestamp
from rich import box
from rich.live import Live
from rich.table import Table


Candles = List[List[List[Union[int, float]]]]


def setup_table() -> Table:
    """Create Rich table layout.

    Returns:
        Table: Include desired description and columns.
    """
    message = """Thank you for using crypto-candlesticks
            Consider supporting your developers
            ETH: 0x06Acb31587a96808158BdEd07e53668d8ce94cFE"""
    table: Table = Table(
        show_header=True,
        caption=message,
        box=box.MINIMAL_HEAVY_HEAD,
        header_style='bold #ffff00',
        title='CRYPTO CANDLESTICKS',
        title_style='bold #54ff00 underline',
        show_lines=True,
        safe_box=True,
        expand=True,
    )
    table_columns = (
        'OPEN',
        'CLOSE',
        'HIGH',
        'LOW',
        'VOLUME',
        'TICKER',
        'INTERVAL',
        'TIME',
    )
    for column in table_columns:
        table.add_column(column, justify='center', no_wrap=True)

    return table


def write_to_console(
    ticker: str,
    interval: str,
    data_downloaded: Candles,
    live: Live,
    table: Table,
) -> Table:
    """Write data to console.

    Args:
        ticker (str): Quote + base currency.
        interval (str): Candlestick interval.
        data_downloaded (Candles): Response from the exchange.
        live (Live): Context manager.
        table (Table): Rich table.

    Returns:
        Table: Updated table to be rendered.
    """
    for row_limit, single_candle in enumerate(data_downloaded[::-1]):
        timestamp = pd.to_datetime(single_candle[0], unit='ms')
        add_row_to_table(ticker, interval, table, single_candle, timestamp)
        max_rows = 15
        if row_limit == max_rows:
            live.update(table)
            break
    live.update(table)
    return table


def add_row_to_table(
    ticker: str,
    interval: str,
    table: Table,
    single_candle: List[List[Union[int, float]]],
    timestamp: Timestamp,
) -> None:
    """Add row to table.

    Args:
        ticker (str): Current ticker.
        interval (str): Current interval.
        table (Table): Table for data. in the terminal
        single_candle (List[List[int  |  float]]): OHLCV
        timestamp (Timestamp): Timestamp of the candle
    """
    table.add_row(
        f'[bold white]{single_candle[2]}[/bold white]',  # Open
        f'[bold white]{single_candle[1]}[/bold white]',  # Close
        f'[bold white]{single_candle[3]}[/bold white]',  # High
        f'[bold white]{single_candle[4]}[/bold white]',  # Low
        f'[bold white]{single_candle[5]}[/bold white]',  # Volume
        f'[bold white]{ticker}[/bold white]',
        f'[bold white]{interval}[/bold white]',
        f'[bold white]{timestamp}[/bold white]',
    )
