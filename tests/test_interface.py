# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, Mock

import pytest
import requests
from click.testing import CliRunner
from pytest_mock import MockerFixture, mocker

from crypto_candlesticks import interface
from crypto_candlesticks.bitfinex_connector.connector import Connector
from crypto_candlesticks.database import SqlDatabase


@pytest.fixture  # type: ignore
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """Exits with a status code of zero."""
    result = runner.invoke(
        interface.main,
        args=[
            "-s",
            "btc",
            "-b",
            "usd",
            "-i",
            "1m",
            "-sd",
            "2020-01-01",
            "-ed",
            "2020-01-01",
        ],
    )
    assert result.exit_code == 0


@pytest.mark.e2e  # type: ignore
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    result = runner.invoke(
        interface.main,
        args=[
            "-s",
            "btc",
            "-b",
            "usd",
            "-i",
            "1m",
            "-sd",
            "2020-01-01",
            "-ed",
            "2020-01-01",
        ],
    )
    assert result.exit_code == 0


def test_main_fails(runner: CliRunner) -> None:
    """Exits with a status code of two."""
    result = runner.invoke(
        interface.main,
        args=[
            "-s",
            "CTT",
            "-b",
            "TTC",
            "-i",
            "20m",
            "-sd",
            "1990-01-01",
            "-ed",
            "3000-01-01",
        ],
    )
    assert result.exit_code == 2


@pytest.mark.e2e  # type: ignore
def test_main_fails_in_production_env(runner: CliRunner) -> None:
    """Exits with a status code of two (end-to-end)."""
    result = runner.invoke(
        interface.main,
        args=[
            "-s",
            "CTT",
            "-b",
            "TTC",
            "-i",
            "20m",
            "-sd",
            "1990-01-01",
            "-ed",
            "3000-01-01",
        ],
    )
    assert result.exit_code == 2


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It exits with a non-zero status code if the request fails."""
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(
        interface.main,
        args=[
            "-s",
            "btc",
            "-b",
            "usd",
            "-i",
            "1m",
            "-sd",
            "2020-01-01",
            "-ed",
            "2020-01-01",
        ],
    )
    assert result.exit_code == 1


def test__repr__():
    db = SqlDatabase("test.db")
    assert db.__repr__() == "Sql database class"
