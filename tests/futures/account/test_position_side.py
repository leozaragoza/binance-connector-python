import responses
from binance.futures import Futures as Client
from tests.util import mock_http_response
from tests.util import random_str

mock_item = {"key_1": "value_1", "key_2": "value_2"}
key = random_str()
secret = random_str()


@mock_http_response(responses.GET, "/fapi/v1/positionSide/dual", mock_item, 200)
def test_change_position_side():
    """Tests the API endpoint position side"""

    client = Client(key, secret)
    response = client.position_side()
    response.should.equal(mock_item)
