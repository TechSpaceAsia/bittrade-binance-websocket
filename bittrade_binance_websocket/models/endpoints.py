from enum import Enum


class BinanceEndpoints(Enum):
    GET_TIME = "/api/v3/time"
    LISTEN_KEY = "/api/v3/userDataStream"
    ISOLATED_MARGIN_LISTEN_KEY = "/sapi/v1/userDataStream/isolated"
    MARGIN_OPEN_ORDERS = "/sapi/v1/margin/openOrders"
    SYMBOL_PRICE_TICKER = "/api/v3/ticker/price"
    SYMBOL_ORDERS_CANCEL = "/api/v3/openOrders"
    CURRENT_OPEN_ORDERS = "/api/v3/openOrders"
