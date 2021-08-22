import responses
from binance.futures import Futures as Client
from tests.util import mock_http_response
from tests.util import random_str

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -1, "msg": "error message"}
key = random_str()
secret = random_str()


@mock_http_response(responses.GET, "/fapi/v1/multiAssetsMargin", mock_item, 200)
def test_get_multi_assets_margin():
    """Tests the API endpoint Get Current Multi-Assets Mode"""

    client = Client(key, secret)
    response = client.get_multi_assets_margin()
    response.should.equal(mock_item)
