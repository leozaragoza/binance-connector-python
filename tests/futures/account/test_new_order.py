from urllib.parse import urlencode

import responses
from binance.futures import Futures as Client
from tests.util import mock_http_response
from tests.util import random_str
from binance.error import ParameterRequiredError

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -1, "msg": "error message"}
key = random_str()
secret = random_str()

params = {
    "symbol": "BTCUSDT",
    "side": "SELL",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 0.002,
    "price": 46000,
    "recvWindow": 1000,
}


@mock_http_response(responses.POST, "/fapi/v1/order", mock_exception, 400)
def test_new_order_without_params():
    """Tests the API endpoint new order without parameter symbol"""

    client = Client(key, secret)
    client.new_order.when.called_with(symbol="", side="", type="")\
        .should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/order\\?symbol=&side=SELL&type=LIMIT", mock_exception, 400)
def test_new_order_without_param_symbol():
    """Tests the API endpoint new order without parameter symbol"""

    client = Client(key, secret)
    client.new_order.when.called_with(symbol="", side="SELL", type="LIMIT")\
        .should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/order\\?symbol=BTCUSDT&side=&type=LIMIT", mock_exception, 400)
def test_new_order_without_param_side():
    """Tests the API endpoint new order without parameter side"""

    client = Client(key, secret)
    client.new_order.when.called_with(symbol="BTCUSDT", side="", type="LIMIT")\
        .should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/order\\?symbol=BTCUSDT&side=SELL&type=", mock_exception, 400)
def test_new_order_without_param_type():
    """Tests the API endpoint new order without parameter type"""

    client = Client(key, secret)
    client.new_order.when.called_with(symbol="BTCUSDT", side="SELL", type="")\
        .should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/order\\?" + urlencode(params), mock_item, 200)
def test_new_order():
    """Tests the API endpoint new order with required params"""
    client = Client(key, secret)
    client.new_order(symbol="BTCUSDT", side="SELL", type="LIMIT", timeInForce="GTC", quantity=0.002, price=46000,
                     recvWindow=1000).should.equal(mock_item)
