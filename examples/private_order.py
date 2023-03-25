import logging
import os
import time
from typing import Callable, Dict, Tuple, cast
from rich.logging import RichHandler
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.output import debug_observer, debug_operator, info_observer
from ccxt import binance
from reactivex import Observable, operators
from bittrade_binance_websocket.channels.book_ticker import (
    parse_book_ticker_ccxt,
    subscribe_book_ticker,
)
from bittrade_binance_websocket.channels.depth import (
    parse_order_book_ccxt,
    subscribe_depth,
)
from bittrade_binance_websocket.connection.private import private_websocket_connection

from bittrade_binance_websocket.events.add_order import add_order
from bittrade_binance_websocket.events.cancel_order import cancel_order
from bittrade_binance_websocket.events.ping import ping
from bittrade_binance_websocket.events.request_response import add_keys
from bittrade_binance_websocket.messages.listen import filter_new_socket_only
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
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

console = RichHandler()
console.setLevel(
    logging.DEBUG
)  # <- if you wish to see subscribe/unsubscribe and raw messages, change to DEBUG
logger = logging.getLogger("bittrade_binance_websocket")
logger.setLevel(logging.DEBUG)
logger.addHandler(console)

key = os.getenv("BINANCE_API_KEY")
secret = os.getenv("BINANCE_SECRET")

socket_connection = private_websocket_connection()

messages = socket_connection.pipe(
    connection_operators.keep_messages_only(),
    operators.share(),  # Usually best to share messages to avoid overhead
)
messages.subscribe(info_observer("ALL MESSAGES", "bittrade_binance_websocket"))
# Subscribe to multiple channels only when socket connects
ready = socket_connection.pipe(
    operators.do_action(print, print, print),
    filter_new_socket_only(),
    operators.do_action(print, print, print),
    add_keys(secret, key),
    operators.replay(1),
    operators.ref_count(),
)

order_request = PlaceOrderRequest(
    symbol="BTCUSDT",
    side=OrderSide.SELL,
    type=OrderType.LIMIT,
    timeInForce=OrderTimeInForceType.GTC,
    quantity=0.010,
    price=52000.00,
    newOrderRespType=OrderResponseType.ACK,
    quoteOrderQty=None,
    stopPrice=None,
    trailingDelta=None,
)

sub1 = ready.pipe(add_order(messages, order_request))
sub = socket_connection.connect()

sub1.subscribe(info_observer("ADD ORDER", "bittrade_binance_websocket"))

time.sleep(10)
sub2 = ready.pipe(add_order(messages, order_request))


def on_next(response: ResponseMessage):
    result = cast(Dict, cast(Dict, response).get("result"))
    logger.info(result)

    request = OrderCancelRequest(
        symbol="BTCUSDT", orderId=result["orderId"], origClientOrderId=None
    )
    ready.pipe(cancel_order(messages, request)).subscribe(
        info_observer("CANCEL ORDER", "bittrade_binance_websocket")
    )


sub2.subscribe(on_next=on_next)

time.sleep(10)
assert sub is not None
sub.dispose()
