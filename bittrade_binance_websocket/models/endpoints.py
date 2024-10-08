from enum import Enum


# https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md
class BinanceEndpoints(Enum):
    SPOT_OPEN_ORDERS = "/api/v3/openOrders"
    ACCOUNT_INFORMATION = "/api/v3/account"
    GET_TIME = "/api/v3/time"
    CROSS_MARGIN_LISTEN_KEY = "/sapi/v1/userDataStream"
    ISOLATED_MARGIN_LISTEN_KEY = "/sapi/v1/userDataStream/isolated"
    MARGIN_SPECIAL_MARGIN_KEY = "/sapi/v1/margin/apiKey"
    MARGIN_SPECIAL_MARGIN_KEY_IP = "/sapi/v1/margin/apiKey/ip"
    MARGIN_SPECIAL_MARGIN_KEY_LIST = "/sapi/v1/margin/api-key-list"
    LISTEN_KEY = "/api/v3/userDataStream"
    MARGIN_OPEN_ORDERS = "/sapi/v1/margin/openOrders"
    MARGIN_ORDER = "/sapi/v1/margin/order"
    MARGIN_MAX_BORROWABLE = "/sapi/v1/margin/maxBorrowable"
    MARGIN_LOAN = "/sapi/v1/margin/loan"
    MARGIN_PORTFOLIO_ACCOUNT_INFORMATION = "/sapi/v1/portfolio/account"
    MARGIN_REPAY = "/sapi/v1/margin/repay"
    MARGIN_FUTURE_INTEREST_RATE = "/sapi/v1/margin/next-hourly-interest-rate"
    MARGIN_INTEREST_HISTORY = "/sapi/v1/margin/interestHistory"
    MARGIN_QUERY_BORROW_REPAY_RECORDS = "/sapi/v1/margin/borrow-repay"
    SPOT_ORDER = "/api/v3/order"
    SPOT_TRADE_LIST = "/api/v3/myTrades"
    MARGIN_TRADE_LIST = "/sapi/v1/margin/myTrades"
    MARGIN_AVAILABLE_INVENTORY = "/sapi/v1/margin/available-inventory"
    QUERY_CROSS_MARGIN_ACCOUNT_DETAILS = "/sapi/v1/margin/account"
    QUERY_ISOLATED_MARGIN_ACCOUNT_DETAILS = "/sapi/v1/margin/isolated/account"
    QUERY_ISOLATED_MARGIN_FEE_DATA = "/sapi/v1/margin/isolatedMarginData"
    QUERY_MAX_TRANSFER_OUT_AMOUNT = "/sapi/v1/margin/maxTransferable"
    QUERY_MARGIN_PRICE_INDEX = "/sapi/v1/margin/priceIndex"
    QUERY_CROSS_MARGIN_FEE_DATA = "/sapi/v1/margin/crossMarginData"
    SYMBOL_PRICE_TICKER = "/api/v3/ticker/price"
    SYMBOL_BOOK_TICKER = "/api/v3/ticker/bookTicker"
    SUBACCOUNT_LIST = "/sapi/v1/sub-account/list"
    SUBACCOUNT_SUMMARY = "/sapi/v1/sub-account/margin/accountSummary"
    SUBACCOUNT_MARGIN_DETAIL = "/sapi/v1/sub-account/margin/account"
    SUBACCOUNT_ASSETS = "/sapi/v3/sub-account/assets"
    SUBACCOUNT_ADD_IP_RESTRICTION = "/sapi/v2/sub-account/subAccountApi/ipRestriction"
    SUBACCOUNT_TRANSFER = "/sapi/v1/sub-account/margin/transfer"
    SUBACCOUNT_UNIVERSAL_TRANSFER = "/sapi/v1/sub-account/universalTransfer"
    SUBACCOUNT_TO_MASTER_TRANSFER = "/sapi/v1/sub-account/transfer/subToMaster"
    SUBACCOUNT_TO_SUBACCOUNT_TRANSFER = "/sapi/v1/sub-account/transfer/subToSub"
    USER_UNIVERSAL_TRANSFER = "/sapi/v1/asset/transfer"
    SPOT_KLINE = "/api/v3/klines"
