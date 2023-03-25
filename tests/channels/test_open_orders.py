from bittrade_binance_websocket.channels.open_orders import is_open_order_message


def test_is_open_order_message():
    # Test a dictionary with the "e" key set to "executionReport"
    x1 = {
        "e": "executionReport",
        "S": "BUY",
        "o": "LIMIT",
        "q": "1.00000000",
        "p": "0.10264410",
    }
    assert is_open_order_message(x1) == True

    # Test a dictionary with the "e" key set to "otherEvent"
    x2 = {
        "e": "otherEvent",
        "S": "SELL",
        "o": "MARKET",
        "q": "2.00000000",
        "p": "0.00000000",
    }
    assert is_open_order_message(x2) == False

    # Test a dictionary with no "e" key
    x3 = {"S": "BUY", "o": "STOP_LOSS", "q": "0.50000000", "p": "0.09000000"}
    assert is_open_order_message(x3) == False

    # Test a dictionary with an empty "e" key
    x4 = {"e": "", "S": "SELL", "o": "MARKET", "q": "3.00000000", "p": "0.00000000"}
    assert is_open_order_message(x4) == False

    # Test a dictionary with a None "e" value
    x5 = {"e": None, "S": "BUY", "o": "LIMIT", "q": "4.00000000", "p": "0.50000000"}
    assert is_open_order_message(x5) == False
