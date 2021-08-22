import responses
from binance.futures import Futures as Client
from tests.util import mock_http_response
from tests.util import random_str
from binance.error import ParameterRequiredError

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -1, "msg": "error message"}
key = random_str()
secret = random_str()


@mock_http_response(responses.POST, "/fapi/v1/multiAssetsMargin", mock_exception, 400)
def test_change_multi_assets_margin_without_param():
    """Tests the API endpoint to change multi assets margin without parameters"""

    client = Client(key, secret)
    client.change_multi_assets_margin.when.called_with("").should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/multiAssetsMargin", mock_item, 200)
def test_change_multi_assets_margin():
    """Tests the API endpoint to change multi assets margin"""

    client = Client(key, secret)
    response = client.change_multi_assets_margin("true")
    response.should.equal(mock_item)
