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
params = {"symbol": "BTCUSDT", "leverage": 20}


@mock_http_response(responses.POST, "/fapi/v1/leverage", mock_exception, 400)
def test_change_leverage_without_params():
    """Tests the API endpoint to change leverage without parameters"""

    client = Client(key, secret)
    client.change_leverage.when.called_with(symbol="", leverage=None).should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/leverage?symbol=&leverage=20", mock_exception, 400)
def test_change_leverage_without_param_symbol():
    """Tests the API endpoint to change leverage without symbol parameter"""

    client = Client(key, secret)
    client.change_leverage.when.called_with(symbol="", leverage=20).should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/leverage?symbol=BTCUSDT", mock_exception, 400)
def test_change_leverage_without_param_leverage():
    """Tests the API endpoint to change leverage without leverage parameter"""

    client = Client(key, secret)
    client.change_leverage.when.called_with(symbol="BTCUSDT", leverage=None).should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/leverage\\?" + urlencode(params), mock_item, 200)
def test_change_leverage():
    """Tests the API endpoint to change leverage"""

    client = Client(key, secret)
    response = client.change_leverage(symbol="BTCUSDT", leverage=20)
    response.should.equal(mock_item)
