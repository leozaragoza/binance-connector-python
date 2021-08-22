import responses

from urllib.parse import urlencode
from tests.util import random_str
from tests.util import mock_http_response
from binance.futures import Futures as Client
from binance.error import ParameterRequiredError, ClientError

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -2011, "msg": "Error message"}

key = random_str()
secret = random_str()

params = {"symbol": "BTCUSDT", "countdownTime": 2000}


@mock_http_response(responses.GET, "/fapi/v1/countdownCancelAll\\?symbol=&count_down_time=2000", mock_exception, 400)
def test_auto_cancel_open_orders_without_symbol():
    """Tests the API endpoint to auto cancel all open orders without symbol"""

    client = Client(key, secret)
    client.auto_cancel_all.when.called_with(symbol="", count_down_time=2000).should.throw(ParameterRequiredError)


@mock_http_response(responses.GET, "/fapi/v1/countdownCancelAll\\?symbol=BTCUSDT&count_down_time=2000", mock_exception,
                    400)
def test_auto_cancel_open_orders_without_count_down_time():
    """Tests the API endpoint to auto cancel all open orders without count down time"""

    client = Client(key, secret)
    client.auto_cancel_all.when.called_with(symbol="BTCUSDT", count_down_time=None).should.throw(ParameterRequiredError)


@mock_http_response(
    responses.POST, "/fapi/v1/countdownCancelAll\\?" + urlencode(params), mock_item, 200
)
def test_auto_cancel_open_orders():
    """Tests the API endpoint to auto cancel all open orders"""

    client = Client(key, secret)

    response = client.auto_cancel_all(symbol="BTCUSDT", count_down_time=2000)
    response.should.equal(mock_item)
