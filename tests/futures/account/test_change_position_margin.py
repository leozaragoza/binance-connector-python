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
params = {"symbol": "BTCUSDT", "amount": 100, "type": 1}


@mock_http_response(responses.POST, "/fapi/v1/positionMargin", mock_exception, 400)
def test_change_position_margin_without_params():
    """Tests the API endpoint to change position margin without parameters"""

    client = Client(key, secret)
    client.change_position_margin.when.called_with(symbol="", amount=None, type=None)\
        .should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/positionMargin\\?symbol=&amount=100&type=1", mock_exception, 400)
def test_change_position_margin_without_param_symbol():
    """Tests the API endpoint to change position margin without symbol parameter"""

    client = Client(key, secret)
    client.change_position_margin.when.called_with(symbol="", amount=100, type=1).should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/positionMargin\\?symbol=BTCUSDT&amount=&type=1", mock_exception, 400)
def test_change_position_margin_without_param_amount():
    """Tests the API endpoint to change margin without amount parameter"""

    client = Client(key, secret)
    client.change_position_margin.when.called_with(symbol="BTCUSDT", amount=None, type=1)\
        .should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/positionMargin\\?symbol=BTCUSDT&amount=100&type=", mock_exception, 400)
def test_change_position_margin_without_param_type():
    """Tests the API endpoint to change margin without type parameter"""

    client = Client(key, secret)
    client.change_position_margin.when.called_with(symbol="BTCUSDT", amount=100, type=None)\
        .should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/positionMargin\\?" + urlencode(params), mock_item, 200)
def test_change_position_margin():
    """Tests the API endpoint to change position margin"""

    client = Client(key, secret)
    response = client.change_position_margin(symbol="BTCUSDT", amount=100, type=1)
    response.should.equal(mock_item)
