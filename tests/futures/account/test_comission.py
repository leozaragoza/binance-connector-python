import responses
from binance.futures import Futures as Client
from tests.util import mock_http_response
from tests.util import random_str
from binance.error import ParameterRequiredError

mock_item = {"key_1": "value_1", "key_2": "value_2"}
key = random_str()
secret = random_str()


@mock_http_response(responses.GET, "/fapi/v1/commissionRate\\?symbol=", mock_item, 200)
def test_commission_without_symbol():
    """Tests the API endpoint commission"""

    client = Client(key, secret)
    client.commission.when.called_with(symbol="").should.throw(ParameterRequiredError)


@mock_http_response(responses.GET, "/fapi/v1/commissionRate\\?symbol=BTCUSDT", mock_item, 200)
def test_commission():
    """Tests the API endpoint commission"""

    client = Client(key, secret)
    response = client.commission(symbol="BTCUSDT")
    response.should.equal(mock_item)
