import responses
from binance.futures import Futures as Client
from tests.util import mock_http_response
from tests.util import random_str
from binance.error import ParameterRequiredError

mock_item = {"key_1": "value_1", "key_2": "value_2"}
mock_exception = {"code": -1, "msg": "error message"}
key = random_str()
secret = random_str()


@mock_http_response(responses.POST, "/fapi/v1/positionSide/dual", mock_exception, 400)
def test_change_position_side_without_param():
    """Tests the API endpoint to change position side without parameters"""

    client = Client(key, secret)
    client.change_position_side.when.called_with("").should.throw(ParameterRequiredError)


@mock_http_response(responses.POST, "/fapi/v1/positionSide/dual", mock_item, 200)
def test_change_position_side():
    """Tests the API endpoint to change position side"""

    client = Client(key, secret)
    response = client.change_position_side("true")
    response.should.equal(mock_item)
