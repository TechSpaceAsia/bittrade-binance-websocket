from typing import Any, Callable, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import order

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(order.SymbolOrderResponseItem)
def margin_create_order_http_factory(
    params: order.PlaceOrderRequest,
):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.MARGIN_CREATE_ORDER,
        params=params.to_dict(),
    )


@http_factory(order.SymbolOrderResponseItem)
def spot_create_order_http_factory(
    params: order.PlaceOrderRequest,
):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.SPOT_CREATE_ORDER,
        params=params.to_dict(),
    )
