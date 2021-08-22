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
params = {"symbol": "BTCUSDT", "marginType": "ISOLATED"}


@mock_http_response(responses.POST, "/fapi/v1/marginType", mock_exception, 400)
def test_change_margin_without_params():
    """Tests the API endpoint to change margin without parameters"""

    client = Client(key, secret)
    client.change_margin.when.called_with(symbol="", margin_type=None).should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/marginType\\?symbol=&marginType=ISOLATED" + urlencode(params), mock_item, 200)
def test_change_margin_without_param_symbol():
    """Tests the API endpoint to change margin without symbol parameter"""

    client = Client(key, secret)
    client.change_margin.when.called_with(symbol="", margin_type="ISOLATED").should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/marginType\\?symbol=BTCUSDT&marginType=", mock_exception, 400)
def test_change_margin_without_param_margin_type():
    """Tests the API endpoint to change margin without marginType parameter"""

    client = Client(key, secret)
    client.change_margin.when.called_with(symbol="BTCUSDT", margin_type=None).should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/marginType\\?" + urlencode(params), mock_item, 200)
def test_change_margin():
    """Tests the API endpoint to change margin type"""

    client = Client(key, secret)
    response = client.change_margin(symbol="BTCUSDT", margin_type="ISOLATED")
    response.should.equal(mock_item)
