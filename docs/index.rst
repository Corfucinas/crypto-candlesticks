The crypto-candlesticks project
====================================

.. toctree::
   :hidden:
   :maxdepth: 1

   examples
   license
   modules

The goal behind this project is to facilitate downloading cryptocurrency candlestick data fast & easily.
Currently only the `Bitfinex <https://www.bitfinex.com/>`_ exchange is supported with more to come in future releases.

The command-line interface is built using `Click <https://click.palletsprojects.com/en/7.x/>`_ which is intuitive and will prompt you for the commands.

Once the data is downloaded, it will be converted and stored in a `.csv, .sqlite3 and .pickle` file convenient for analysis.
The data will include the `Open, High, Low, Close` of the candles and the `volume` during the `interval`.

Installation
-----------------

To install the Crypto-candlesticks project,
run this command in your terminal:

.. code-block:: console

   $ pip install crypto-candlesticks

Or if you are using `Poetry <https://python-poetry.org/>`_:

.. code-block:: console

    $ poetry add crypto-candlesticks

Usage
-----

crypto-candlesticks can be used the following way:

.. code-block:: python

    crypto - candlesticks
    "Welcome, what data do you wish to download?"

Which will prompt you for the arguments:

::

    Cryptocurrency symbol to download (ie. BTC, ETH, LTC):
    Base pair:
    Interval to download the candlestick data:
    Date to start downloading the data (ie. YYYY-MM-DD):
    Date up to the data will be downloaded (ie. YYYY-MM-DD):

Or you can pass the arguments yourself and skip the prompt:

.. code-block:: python

   crypto - candlesticks[OPTIONS]

.. option:: -s <symbol>, --symbol <symbol>

   The ticker you wish to download,
   currently, only data from the Bitfinex exchange
   is supported.
   (e.g. [ BTC | ETH | LTC ] etc.)

.. option:: -b <base currency>, --base_currency <base currency>

    The base pair for the ticker.
    (e.g. [ USD | USDT | EUR | CNHT | GBP | JPY | DAI | BTC | EOS | ETH | XCHF | USTF0 ])

.. option:: -i <interval>, --interval <interval>

    The interval for each bar.
    (e.g. [ 1m | 5m | 15m | 30m | 1h | 3h | 6h | 12h | 1D | 7D | 14D | 1M ])

.. option:: -sd <start date>, --start_date <start date>

    YYYY, MM, DD from which the candlestick data
    will start.
    (e.g. [2018-01-01])

.. option:: -ed <end date>, --end date <end date>

    YYYY, MM, DD up to which the candlestick
    data will be downloaded.
    (e.g. [2020-01-01])

.. option:: --help

   Display a short usage message and exit.
