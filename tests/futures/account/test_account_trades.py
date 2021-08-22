import responses
from binance.futures import Futures as Client
from tests.util import mock_http_response
from tests.util import random_str
from binance.error import ParameterRequiredError

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -1, "msg": "error message"}
key = random_str()
secret = random_str()


@mock_http_response(responses.GET, "/fapi/v1/userTrades\\?symbol=", mock_exception, 400)
def test_account_trades_without_symbol():
    """Tests the API endpoint account trades without symbol"""

    client = Client(key, secret)
    client.account_trades.when.called_with(symbol="").should.throw(ParameterRequiredError)


@mock_http_response(responses.GET, "/fapi/v1/userTrades\\?symbol=BTCUSDT", mock_item, 200)
def test_account_trades():
    """Tests the API endpoint account trades """

    client = Client(key, secret)
    response = client.account_trades(symbol="BTCUSDT")
    response.should.equal(mock_item)
