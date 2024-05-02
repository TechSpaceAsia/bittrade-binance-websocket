from typing import Any, Callable

from reactivex import Observable, just, throw
from reactivex import operators
import requests
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request

from bittrade_binance_websocket.connection import http



def create_special_margin_api_key_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def create_special_margin_api_key_http(name: str, public_key: str, ips: list[str], symbol: str | None = None):
        def subscribe(observer, scheduler=None):
            params = {
                "apiName": name,
            }
            if ips:
                params["ip"] = ",".join(ips)
            if symbol:
                params["symbol"] = symbol
            if public_key:
                params["publicKey"] = public_key
            endpoint = endpoints.BinanceEndpoints.MARGIN_SPECIAL_MARGIN_KEY
            req = request.RequestMessage(
                method="POST",
                endpoint=endpoint,
                params=params,
            )
            return http.send_request(
                add_token(
                    http.prepare_request(req)
                )
            ).subscribe(observer, scheduler)
        return Observable(subscribe)
    
    return create_special_margin_api_key_http
