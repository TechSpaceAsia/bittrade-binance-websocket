import logging
import os
import time
from typing import Callable, Dict, Tuple, cast
from uuid import uuid4
import reactivex
from rich.logging import RichHandler
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.output import debug_observer, debug_operator, info_observer
from ccxt import binance
from reactivex import Observable, operators
from bittrade_binance_websocket.connection.private import private_websocket_connection
from elm_framework_helpers.config import read_config

from bittrade_binance_websocket.events.add_order import add_order
from bittrade_binance_websocket.events.cancel_order import cancel_order
from bittrade_binance_websocket.events.ping import ping
from bittrade_binance_websocket.events.request_response import add_keys
from bittrade_binance_websocket.framework.framework import get_framework
from bittrade_binance_websocket.messages.listen import filter_new_socket_only
from bittrade_binance_websocket.models.order import (
    OrderCancelRequest,
    OrderResponseType,
    OrderSide,
    OrderTimeInForceType,
    OrderType,
    PlaceOrderRequest,
    PlaceOrderResponse,
)
from bittrade_binance_websocket.models.response_message import ResponseMessage
from IPython.terminal import embed


console = RichHandler()
console.setLevel(
    logging.DEBUG
)  # <- if you wish to see subscribe/unsubscribe and raw messages, change to DEBUG
logger = logging.getLogger("")
# logger = logging.getLogger("bittrade_binance_websocket")
logger.setLevel(logging.DEBUG)
logger.addHandler(console)

key = read_config("key")
secret = read_config("secret")


def add_keys(x):
    x.key = key
    x.secret = secret
    return x


framework = get_framework(spot_trade_signer=add_keys, load_markets=False)
framework.spot_trade_socket_messages.subscribe(print, print, print)


order_request = PlaceOrderRequest(
    symbol="BTCUSDT",
    side=OrderSide.BUY,
    type=OrderType.LIMIT_MAKER,
    timeInForce=None,
    quantity="0.001",
    price="27000",
    newOrderRespType=OrderResponseType.FULL,
    quoteOrderQty=None,
    stopPrice=None,
    trailingDelta=None,
    newClientOrderId=str(uuid4()),
)

ready = framework.spot_trade_guaranteed_sockets.pipe(
    operators.filter(lambda x: x is not None), operators.take(1), operators.share()
)

framework.spot_trade_socket_messages.subscribe(
    info_observer("SPOT TRADE", "bittrade_binance_websocket")
)


sub = framework.spot_trade_socket_bundles.connect()

# Can be triggered manually or part of a concat with ready etc
# framework.spot_order_create(order_request).subscribe(print, print, print)

embed.embed()

sub.dispose()
