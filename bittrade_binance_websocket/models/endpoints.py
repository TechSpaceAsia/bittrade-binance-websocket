from enum import Enum


class BinanceEndpoints(Enum):
    CURRENT_OPEN_ORDERS = "/api/v3/openOrders"
    GET_TIME = "/api/v3/time"
    ISOLATED_MARGIN_LISTEN_KEY = "/sapi/v1/userDataStream/isolated"
    LISTEN_KEY = "/api/v3/userDataStream"
    MARGIN_OPEN_ORDERS = "/sapi/v1/margin/openOrders"
    QUERY_CROSS_MARGIN_ACCOUNT_DETAILS = "/sapi/v1/margin/account"
    SYMBOL_ORDERS_CANCEL = "/api/v3/openOrders"
    SYMBOL_PRICE_TICKER = "/api/v3/ticker/price"
