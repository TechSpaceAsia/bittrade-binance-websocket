import requests
from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import listen_key
import reactivex

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory

@http_factory(lambda: request.RequestMessage(
    method="POST",
    endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
), listen_key.CreateListenKeyResponse)
def get_listen_key(request: requests.models.Request):
    return http.generate_add_api_key()(request)
