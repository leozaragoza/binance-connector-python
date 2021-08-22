import responses

from urllib.parse import urlencode
from tests.util import random_str
from tests.util import mock_http_response
from binance.futures import Futures as Client
from binance.error import ParameterRequiredError, ClientError

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -1105, "msg": 'Parameter "orderId" was empty.'}

key = random_str()
secret = random_str()

orderIdList = "1234567"
origClientOrderId = "2345678"

params = {
    "symbol": "BTCUSDT",
    "orderId": orderIdList,
    "origClientOrderId": origClientOrderId,
    "recvWindow": 1000,
}


@mock_http_response(responses.DELETE, f"/fapi/v1/batchOrders\\?symbol=&orderIdList={orderIdList}", mock_exception, 400)
def test_cancel_batch_order_without_symbol():
    """Tests the API endpoint to cancel batch order without symbol"""

    client = Client(key, secret)
    client.cancel_batch_orders.when.called_with("").should.throw(ParameterRequiredError)


@mock_http_response(responses.DELETE, "/fapi/v1/batchOrders\\?symbol=BTCUSDT&orderIdList=", mock_exception, 400)
def test_cancel_batch_order_without_order_id():
    """Tests the API endpoint to cancel batch order without provide order id list"""

    client = Client(key, secret)
    client.cancel_batch_orders.when.called_with(symbol="BTCUSDT", orderIdList="").should.throw(ClientError)


@mock_http_response(
    responses.DELETE, "/fapi/v1/batchOrders\\?symbol=BTCUSDT&orderIdList=" + orderIdList, mock_item, 200
)
def test_cancel_batch_order_with_order_id():
    """Tests the API endpoint to batch cancel order"""

    client = Client(key, secret)
    response = client.cancel_batch_orders("BTCUSDT", orderIdList=orderIdList)
    response.should.equal(mock_item)


@mock_http_response(
    responses.DELETE, "/fapi/v1/batchOrders\\?" + urlencode(params), mock_item, 200
)
def test_cancel_batch_order_with_more_params():
    """Tests the API endpoint to batch cancel order with other parameters"""

    client = Client(key, secret)
    response = client.cancel_batch_orders(**params)
    response.should.equal(mock_item)
