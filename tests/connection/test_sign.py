import hmac

import pytest
from bittrade_binance_websocket.connection.sign import encode_query_string, get_signature, to_sorted_qs

@pytest.fixture
def request_params():
    return {
        'type': 'LIMIT',
        'timestamp': '1645423376532',
        'timeInForce': 'GTC',
        'symbol': 'BTCUSDT',
        'side': 'SELL',
        'recvWindow': 100,
        'quantity': '0.01000000',
        'price': '52000.00',
        'newOrderRespType': 'ACK',
        'apiKey': 'vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A'
    }

def test_to_sorted_qs(request_params):
    sorted = to_sorted_qs(request_params)
    assert sorted == (('apiKey', 'vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A'), ('newOrderRespType', 'ACK'), ('price', '52000.00'), ('quantity', '0.01000000'), ('recvWindow', 100), ('side', 'SELL'), ('symbol', 'BTCUSDT'), ('timeInForce', 'GTC'), ('timestamp', '1645423376532'), ('type', 'LIMIT'))

def test_encode_qs(request_params):
    sorted = to_sorted_qs(request_params)
    qs = encode_query_string(sorted)
    assert qs == 'apiKey=vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A&newOrderRespType=ACK&price=52000.00&quantity=0.01000000&recvWindow=100&side=SELL&symbol=BTCUSDT&timeInForce=GTC&timestamp=1645423376532&type=LIMIT'

def test_generate_signature(request_params):
    sorted = to_sorted_qs(request_params)
    qs = encode_query_string(sorted)

    sign = get_signature('NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j')
    hash_signed = sign(qs)
    assert hash_signed == 'cc15477742bd704c29492d96c7ead9414dfd8e0ec4a00f947bb5bb454ddbd08a'