from typing import Any, Callable

from reactivex import Observable, just, throw
from reactivex import operators
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import order

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(dict)
def get_account_information_http_factory(
    is_margin: bool=False, is_isolated: bool = False, symbols: list[str] | None = None
):
    params = {}
    if is_isolated and symbols:
        params["symbols"] = ",".join(symbols)
    endpoint = endpoints.BinanceEndpoints.ACCOUNT_INFORMATION
    if is_margin:
        endpoint = endpoints.BinanceEndpoints.QUERY_CROSS_MARGIN_ACCOUNT_DETAILS
        if is_isolated:
            endpoint = endpoints.BinanceEndpoints.QUERY_ISOLATED_MARGIN_ACCOUNT_DETAILS
    return request.RequestMessage(
        method="GET",
        endpoint=endpoint,
        params=params,
    )
