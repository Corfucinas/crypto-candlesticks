# -*- coding: utf-8 -*-
"""Test interface for crypto candlesticks."""
from time import perf_counter, sleep
from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from crypto_candlesticks import interface


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.mark.e2e
def test_main_succeeds_1m(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '1m',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 1m test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'1 minutes data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_5m(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '5m',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 5m test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'5 minutes data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_15m(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '15m',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 15m test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'15 minutes data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_30m(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '30m',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 30m test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'30 minutes data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_1h(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '1h',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 1h test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'1 hour data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_3h(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '3h',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'3 hours data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_6h(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '6h',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 6 hours test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'6 hours data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_12h(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '6h',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 12 hours test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'12 hours data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_1D(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 1 day test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'1 day data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_7D(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '7D',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 7 day test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'7 day data could not be downloaded {error}')
        raise


@pytest.mark.e2e
def test_main_succeeds_14D(runner: CliRunner) -> None:
    """Exits with a status code of zero."""
    sleep(10)
    start = perf_counter()
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '14D',
            '-sd',
            '2020-11-01',
            '-ed',
            '2021-01-01',
        ],
    )
    end = perf_counter()
    print(f'Time to complete the 7 day test: {end - start}')
    try:
        assert test_result.exit_code == 0
    except AssertionError as error:
        print(f'7 day data could not be downloaded {error}')
        raise


def test_main_fails(runner: CliRunner) -> None:
    """Exits with a status code of two."""
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'CTT',
            '-b',
            'TTC',
            '-i',
            '20m',
            '-sd',
            '1990-01-01',
            '-ed',
            '3000-01-01',
        ],
    )
    assert test_result.exit_code == 2


@pytest.mark.e2e
def test_main_fails_in_production_env(runner: CliRunner) -> None:
    """Exits with a status code of two (end-to-end)."""
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'CTT',
            '-b',
            'TTC',
            '-i',
            '20m',
            '-sd',
            '1990-01-01',
            '-ed',
            '3000-01-01',
        ],
    )
    assert test_result.exit_code == 2


def test_main_fails_on_request_error(
    runner: CliRunner,
    mock_requests_get: Mock,
) -> None:
    """It exits with a non-zero status code if the request fails."""
    mock_requests_get.side_effect = Exception('Boom')
    test_result = runner.invoke(
        interface.main,
        args=[
            '-s',
            'btc',
            '-b',
            'usd',
            '-i',
            '1m',
            '-sd',
            '2020-01-01',
            '-ed',
            '2020-01-01',
        ],
    )
    assert test_result.exit_code == 1
