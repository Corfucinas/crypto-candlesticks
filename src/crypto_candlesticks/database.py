# -*- coding: utf-8 -*-
"""Sqlite database class."""

import sqlite3
from typing import List, TypeVar

import click

Sql = TypeVar('Sql', bound='SqlDatabase')


class SqlDatabase(object):
    """SqlDatabase main class for storing the candlestick data in SQL."""

    __slots__ = (
        '_databasefile',
        '_conn',
        '_cursor',
        '_encoding',
        '_synchronous',
        '_journal',
        '_table',
    )

    def __init__(self: Sql, databasefile: str) -> None:
        """Database init."""
        self._databasefile = databasefile
        self._conn = sqlite3.connect(self._databasefile)
        self._cursor = self._conn.cursor()
        self._encoding = self._cursor.execute("PRAGMA encoding='UTF-8';")
        self._synchronous = self._cursor.execute('PRAGMA synchronous=0;')
        self._journal = self._cursor.execute('PRAGMA journal_mode=WAL;')
        self._table = self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS "Candlestick"(
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Timestamp REAL NOT NULL,
                Open REAL NOT NULL,
                Close REAL NOT NULL,
                High REAL NOT NULL,
                Low REAL NOT NULL,
                Volume REAL NOT NULL,
                Ticker TEXT NOT NULL,
                Interval TEXT NOT NULL
                )""",
        )

    def __repr__(self: Sql) -> str:
        """Database repr."""
        return 'Sql database class'

    def insert_candlesticks(
        self: Sql, candlestick_info: List[float], ticker: str, interval: str,
    ) -> None:
        """Writes the candlestick data into a SQL table.

        Args:
            candlestick_info (List[float]): A list of floats containing OHLC.
            ticker (str): Ticker of the candle.
            interval (str): Period downloaded.

        Raises:
            sqlite3.Error: Exception that prevented to write the data.

        """
        try:
            for candle in candlestick_info:
                with self._conn:
                    self._cursor.execute(
                        'INSERT INTO Candlestick VALUES \
                        (:ID, :Timestamp, :Open, \
                        :Close, :High, :Low, \
                        :Volume, :Ticker, :Interval)',
                        {
                            'ID': None,
                            'Timestamp': candle[0],  # type: ignore
                            'Open': candle[2],  # type: ignore
                            'Close': candle[1],  # type: ignore
                            'High': candle[3],  # type: ignore
                            'Low': candle[4],  # type: ignore
                            'Volume': candle[5],  # type: ignore
                            'Ticker': ticker,
                            'Interval': interval,
                        },
                    )
        except (sqlite3.Error) as sqlite_error:
            click.echo(('Failed to write data to Database', sqlite_error))
            raise
