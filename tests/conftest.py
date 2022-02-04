# -*- coding: utf-8 -*-
"""Package-wide test fixtures."""
# built-in
from unittest.mock import Mock

# external
import pytest
from _pytest.config import Config
from pytest_mock import MockerFixture


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line('markers', 'e2e: mark as end-to-end test.')


@pytest.fixture
def mock_requests_get(mocker: MockerFixture) -> Mock:
    """Fixture for mocking requests.get."""
    mock = mocker.patch('requests.get')
    mock.return_value.__enter__.return_value.json.return_value = {
        'btc': 'usd',
        '400': [],
    }
    return mock
