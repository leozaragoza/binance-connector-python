import responses

from urllib.parse import urlencode
from tests.util import random_str
from tests.util import mock_http_response
from binance.futures import Futures as Client
from binance.error import ParameterRequiredError, ClientError

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -2011, "msg": "unknown order sent"}

key = random_str()
secret = random_str()

orderId = "1234567"
origClientOrderId = "2345678"

params = {"symbol": "BTCUSDT", "recvWindow": 1000}


@mock_http_response(responses.GET, "/fapi/v1/allOpenOrders\\?symbol=", mock_exception, 400)
def test_cancel_open_orders_without_symbol():
    """Tests the API endpoint to cancel all open orders without symbol"""

    client = Client(key, secret)
    client.cancel_all_orders.when.called_with("").should.throw(ParameterRequiredError)


@mock_http_response(
    responses.DELETE, "/fapi/v1/allOpenOrders\\?symbol=BTCUSDT", mock_exception, 400
)
def test_cancel_open_orders_when_no_open_orders():
    """Tests the API endpoint to cancel all open orders when there is no open order"""

    client = Client(key, secret)
    client.cancel_all_orders.when.called_with("BTCUSDT").should.throw(ClientError)


@mock_http_response(
    responses.DELETE, "/fapi/v1/allOpenOrders\\?" + urlencode(params), mock_item, 200
)
def test_cancel_open_orders():
    """Tests the API endpoint to cancel all open orders"""

    client = Client(key, secret)
    response = client.cancel_all_orders("BTCUSDT", recvWindow=1000)
    response.should.equal(mock_item)
