#!/usr/bin/env python

import logging
from binance.futures import Futures as Client
from binance.lib.utils import config_logging

config_logging(logging, logging.DEBUG)

key = ""
secret = ""

client = Client(key, secret, base_url="https://testnet.binancefuture.com")

logging.info(client.commission(symbol="BTCUSDT"))
