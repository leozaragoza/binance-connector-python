from binance.error import ParameterRequiredError
from binance.futures import Futures as Client
import responses

from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -2011, "msg": "unknown order sent"}

key = random_str()
secret = random_str()

params = {"symbol": "BTCUSDT", "recvWindow": 1000}


@mock_http_response(responses.GET, "/fapi/v1/allOrders?symbol=", mock_exception, 400)
def test_get_all_orders_without_symbol():
    """Tests the API endpoint to get all orders"""

    client = Client(key, secret)
    client.get_all_orders.when.called_with(symbol="").should.throw(ParameterRequiredError)


@mock_http_response(
    responses.GET, "/fapi/v1/allOrders\\?" + urlencode(params), mock_item, 200
)
def test_get_all_orders_for_one_pair():
    """Tests the API endpoint to get all orders for one pair"""

    client = Client(key, secret)
    response = client.get_all_orders(**params)
    response.should.equal(mock_item)
