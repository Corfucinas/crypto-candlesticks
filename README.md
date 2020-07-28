# crypto-candlesticks 📈

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
![Tests](https://github.com/Corfucinas/crypto-candlesticks/workflows/Tests/badge.svg)
![Codecov](https://github.com/Corfucinas/crypto-candlesticks/workflows/Codecov/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/crypto-candlesticks/badge/?version=latest)](https://crypto-candlesticks.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/crypto-candlesticks.svg)](https://pypi.org/project/crypto-candlesticks/)

---

The goal behind this project is to facilitate downloading cryptocurrency candlestick data fast & simple.
Currently only the [Bitfinex](https://www.bitfinex.com/) exchange is supported with more to come in future releases.

The command-line interface is built using [Click](https://click.palletsprojects.com/en/7.x/), which is intuitive and will prompt you for the commands.

Once the data is downloaded, it will be converted and stored in a `.csv, .sqlite3 and .pickle` file for convenient analysis.
The data will include the `Open, High, Low, Close` of the candles and the `volume` during the `interval`.

## Installation 💻

To install the Crypto-candlesticks project,
run this command in your terminal:

```bash
   pip install crypto-candlesticks
```

Or if you are using [Poetry](https://python-poetry.org/)

```bash
    poetry add crypto-candlesticks
```

### Usage

crypto-candlesticks can be used the following way:

```bash
    $ crypto-candlesticks
    "Welcome, what data do you wish to download?"
```

Which will prompt the following:

```text
    Cryptocurrency symbol to download (ie. BTC, ETH, LTC):
    Base pair:
    Interval to download the candlestick data:
    Date to start downloading the data (ie. YYYY-MM-DD):
    Date up to the data will be downloaded (ie. YYYY-MM-DD):
```

Or you can pass the arguments yourself and skip the prompt:

```text
   crypto-candlesticks [OPTIONS]

   -s <symbol>, --symbol <symbol>

   The ticker you wish to download,
   currently, only data from the Bitfinex exchange
   is supported.
   (e.g. [BTC|ETH|LTC] etc.)

   -b <base currency>, --base_currency <base currency>

    The base pair for the ticker.
    (e.g. [USD|USDT|EUR|CNHT|GBP|JPY|DAI|BTC|EOS|ETH|XCHF|USTF0])

   -i <interval>, --interval <interval>

    The interval for each bar.
    (e.g. [1m|5m|15m|30m|1h|3h|6h|12h|1D|7D|14D|1M])

   -sd <start date>, --start_date <start date>

    YYYY, MM, DD from which the candlestick data
    will start.
    (e.g. [2018-01-01])

   -ed <end date>, --end date <end date>

    YYYY, MM, DD up to which the candlestick
    data will be downloaded.
    (e.g. [2020-01-01])

   --help

   Display a short usage message and exit.
```

#### Example output for CSV ✅

| Open     | Close     | High   | Low       | Volume    | Ticker  | Date       | Time     |
|----------|-----------|--------|-----------|-----------|---------|------------|----------|
| 7203     | 7201      | 7203.7 | 7200.1    | 9.404174  | BTC/USD | 12/31/2019 | 16:00:00 |
| 7201     | 7223.6    | 7223.6 | 7201      | 7.9037398 | BTC/USD | 12/31/2019 | 16:01:00 |
| 7224.4   | 7225      | 7225.5 | 7224.4    | 0.4799298 | BTC/USD | 12/31/2019 | 16:02:00 |
| 7224.981 | 7225.9    | 7225.9 | 7224.981  | 0.9294573 | BTC/USD | 12/31/2019 | 16:03:00 |
| 7225.862 | 7225.7295 | 7225.9 | 7225.7295 | 0.2913202 | BTC/USD | 12/31/2019 | 16:04:00 |
| 7225.7   | 7225.8673 | 7225.9 | 7225.2973 | 1.0319704 | BTC/USD | 12/31/2019 | 16:05:00 |

#### Example output for SQL (the timestamp is shown in milliseconds) ✅

| ID | Timestamp       | Open          | Close         | High          | Low           | Volume     | Ticker | Interval |
|----|-----------------|---------------|---------------|---------------|---------------|------------|--------|----------|
| 1  | 1577868000000.0 | 7205.7        | 7205.8        | 7205.8        | 7205.7        | 0.07137942 | BTCUSD | 1m       |
| 2  | 1577867940000.0 | 7205.70155305 | 7205.8        | 7205.8        | 7205.70155305 | 0.035      | BTCUSD | 1m       |
| 3  | 1577867880000.0 | 7205.7        | 7205.70155305 | 7205.70155305 | 7205.7        | 0.025      | BTCUSD | 1m       |
| 4  | 1577867820000.0 | 7205.75299748 | 7205.75299748 | 7205.75299748 | 7205.7        | 0.075      | BTCUSD | 1m       |
| 5  | 1577867760000.0 | 7205.75299748 | 7205.2        | 7206.3        | 7205.2        | 0.005      | BTCUSD | 1m       |
| 6  | 1577867700000.0 | 7205.2        | 7205.2        | 7205.2        | 7205.2        | 4.5802     | BTCUSD | 1m       |

##### Contributing 👋

Feel free to open an [issue](https://github.com/Corfucinas/crypto-candlesticks/issues/new) or [pull request](https://github.com/Corfucinas/crypto-candlesticks/pulls).
