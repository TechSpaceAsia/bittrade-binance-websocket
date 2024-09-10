import time
from expression import curry_flip
import reactivex
from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import request, endpoints
from bittrade_binance_websocket.models.message import UserFeedMessage
from bittrade_binance_websocket.models.rest import depth


@curry_flip(1)
def parse_to_userfeedmessage(
    response_data: depth.Depth,
    params: depth.DepthRequest
) -> UserFeedMessage:
    return {
        "E": time.time(),
        "s": params.symbol,
        "b": response_data.get("bids"),
        "a": response_data.get("asks"),
        "u": response_data.get("lastUpdateId"),
    }


def query_depth_http(
    params: depth.DepthRequest,
) -> reactivex.Observable[depth.Depth]:
    return http.send_request(
        http.prepare_request(
            request.RequestMessage(
                method="GET",
                endpoint=(endpoints.BinanceEndpoints.DEPTH),
                params=params.to_dict(),
            )
        )
    )
