from bittrade_binance_websocket.models.order import PlaceOrderRequest


def test_to_dict():
    # Create a PlaceOrderRequest instance with some values
    order_request = PlaceOrderRequest(
        symbol="BTCUSD",
        side="BUY",
        type="LIMIT",
        timeInForce="GTC",
        price=10000,
        quoteOrderQty=None,
        stopPrice=None,
        trailingDelta=None,
        quantity=0.1,
        is_margin=True,
        isIsolated=True,
    )

    # Call the to_dict method and check the result
    expected_result = {
        "symbol": "BTCUSD",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "price": 10000,
        "quantity": 0.1,
        "isIsolated": True,
    }
    assert order_request.to_dict() == expected_result

    # Change the isIsolated attribute and check that the result is updated
    order_request.isIsolated = False
    expected_result = {
        "symbol": "BTCUSD",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "price": 10000,
        "quantity": 0.1,
        "isIsolated": False,
    }
    assert order_request.to_dict() == expected_result

    # Change the is_margin attribute and check that the result is updated
    order_request.is_margin = False
    expected_result = {
        "symbol": "BTCUSD",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "price": 10000,
        "quantity": 0.1,
    }
    assert order_request.to_dict() == expected_result
