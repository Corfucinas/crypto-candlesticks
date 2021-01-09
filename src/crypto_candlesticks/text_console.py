# -*- coding: utf-8 -*-
"""Display data in the CLI using Rich."""
from typing import List, Union

from rich import box
from rich.live import Live
from rich.table import Table

Candles = List[List[List[Union[int, float]]]]


def setup_table() -> Table:
    """Create Rich table layout.

    Returns:
        Table: Include desired description and columns
    """
    table = Table(
        show_header=True,
        box=box.MINIMAL_HEAVY_HEAD,
        header_style="bold #f8e020",
        title="[bold green]CRYPTO CANDLESTICKS[bold green]",
    )

    table.add_column("Open", justify="center")
    table.add_column("Close", justify="center")
    table.add_column("High", justify="center")
    table.add_column("Low", justify="center")
    table.add_column("Volume", justify="center")
    table.add_column("Ticker", justify="center")
    table.add_column("Interval", justify="center")
    table.add_column("Time", justify="center")

    return table


def write_to_column(
    table: Table,
    ticker: str,
    interval: str,
    data_downloaded: Candles,
    live: Live,
) -> Table:
    """Write data to console.

    Args:
        table (Table): [description]
        ticker (str): [description]
        interval (str): [description]
        data_downloaded (Candles): [description]
        live (Live): [description]

    Returns:
        Table: [description]
    """
    for row_limit, single_candle in enumerate(data_downloaded):
        table.add_row(
            f"{single_candle[2]}",  # Open
            f"{single_candle[1]}",  # Close
            f"{single_candle[3]}",  # High
            f"{single_candle[4]}",  # Low
            f"{single_candle[5]}",  # Volume
            ticker,
            interval,
            f"[bold]{single_candle[0]}[/bold]",
        )
        if row_limit == 20:
            live.update(setup_table())
            live.refresh()
            live.update(table)
            live.refresh()
            break
    return table
