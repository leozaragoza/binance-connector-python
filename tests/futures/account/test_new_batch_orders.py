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

batch_orders = [
    {
        "symbol": "ETHUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": 1,
        "price": 3200
    }
]


@mock_http_response(responses.POST, "/fapi/v1/batchOrders\\?batchOrders=", mock_exception, 400)
def test_new_batch_order_without_params():
    """Tests the API endpoint new batch order without parameters"""

    client = Client(key, secret)
    client.new_batch_orders.when.called_with(batch_orders="")\
        .should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/batchOrders", mock_item, 200)
def test_new_batch_order():
    """Tests the API endpoint new batch order with required params"""

    client = Client(key, secret)
    client.new_batch_orders(batch_orders=batch_orders).should.equal(mock_item)

