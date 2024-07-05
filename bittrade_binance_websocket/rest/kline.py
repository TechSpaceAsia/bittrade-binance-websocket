from typing import Any, Callable, List, Optional, cast

from reactivex import Observable
import requests

from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import kline

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


def get_kline_http(params: kline.KlineRequest):
    def subscribe(observer, scheduler=None):
        req = request.RequestMessage(
            method="GET",
            endpoint=endpoints.BinanceEndpoints.MARGIN_ORDER
            if params.is_margin
            else endpoints.BinanceEndpoints.SPOT_ORDER,
            params=params.to_dict(),
        )
        return http.send_request(http.prepare_request(req)).subscribe(
            observer, scheduler
        )
    return cast(Observable[List[Any]], Observable(subscribe))
