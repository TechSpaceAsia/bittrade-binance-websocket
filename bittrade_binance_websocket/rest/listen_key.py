from typing import Dict
import requests
from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import listen_key

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(listen_key.CreateListenKeyResponse)
def get_listen_key_http_factory():
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
    )


@http_factory(listen_key.CreateListenKeyResponse)
def ping_listen_key_http_factory(key: str):
    return request.RequestMessage(
        method="PUT",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
        params={
            "listenKey": key,
        },
    )


@http_factory(listen_key.CreateListenKeyResponse)
def get_active_listen_key_http_factory(key: str):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
    )


@http_factory(listen_key.CreateListenKeyResponse)
def close_listen_key_http_factory(key: str):
    return request.RequestMessage(
        method="DELETE",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
        params={
            "listenKey": key,
        },
    )
