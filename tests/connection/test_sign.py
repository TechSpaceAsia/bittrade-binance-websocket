import hmac

import pytest
from bittrade_binance_websocket.connection.sign import (
    encode_query_string,
    get_signature,
    to_sorted_qs,
)
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket


@pytest.fixture
def request_params():
    return {
        "type": "LIMIT",
        "timestamp": "1645423376532",
        "timeInForce": "GTC",
        "symbol": "BTCUSDT",
        "side": "SELL",
        "recvWindow": 100,
        "quantity": "0.01000000",
        "price": "52000.00",
        "newOrderRespType": "ACK",
        "apiKey": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
    }


def test_to_sorted_qs(request_params):
    sorted = to_sorted_qs(request_params)
    assert sorted == (
        ("apiKey", "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A"),
        ("newOrderRespType", "ACK"),
        ("price", "52000.00"),
        ("quantity", "0.01000000"),
        ("recvWindow", 100),
        ("side", "SELL"),
        ("symbol", "BTCUSDT"),
        ("timeInForce", "GTC"),
        ("timestamp", "1645423376532"),
        ("type", "LIMIT"),
    )


def test_encode_qs(request_params):
    sorted = to_sorted_qs(request_params)
    qs = encode_query_string(sorted)
    assert (
        qs
        == "apiKey=vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A&newOrderRespType=ACK&price=52000.00&quantity=0.01000000&recvWindow=100&side=SELL&symbol=BTCUSDT&timeInForce=GTC&timestamp=1645423376532&type=LIMIT"
    )
    "apiKey=vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A&newOrderRespType=ACK&price=52000.00&quantity=0.01000000&recvWindow=100&side=SELL&symbol=BTCUSDT&timeInForce=GTC&timestamp=1645423376532&type=LIMIT"


def test_generate_signature(request_params):
    sorted = to_sorted_qs(request_params)
    qs = encode_query_string(sorted)

    sign = get_signature(
        "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
    )
    hash_signed = sign(qs)
    assert (
        hash_signed
        == "cc15477742bd704c29492d96c7ead9414dfd8e0ec4a00f947bb5bb454ddbd08a"
    )


def test_prepared_request(request_params):
    message = {"id": "abc", "method": "order.place", "params": request_params}

    websocket = EnhancedWebsocket(None)
    websocket.key = "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A"
    websocket.secret = (
        "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
    )

    # Monkey patch the timestamp
    websocket.get_timestamp = lambda: "1645423376532"

    id, json_string = websocket.prepare_request(message, sign=True)

    assert id == "abc"
    assert (
        json_string
        == b'{"id":"abc","method":"order.place","params":{"type":"LIMIT","timestamp":"1645423376532","timeInForce":"GTC","symbol":"BTCUSDT","side":"SELL","recvWindow":100,"quantity":"0.01000000","price":"52000.00","newOrderRespType":"ACK","apiKey":"vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A","signature":"cc15477742bd704c29492d96c7ead9414dfd8e0ec4a00f947bb5bb454ddbd08a"}}'
    )
