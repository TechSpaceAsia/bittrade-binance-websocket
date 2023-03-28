import logging
from uuid import uuid4
from rich.logging import RichHandler
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.output import debug_observer, debug_operator, info_observer
from reactivex import Observable, operators
from bittrade_binance_websocket.connection.private import private_websocket_connection
from elm_framework_helpers.config import read_config

from bittrade_binance_websocket.events.add_order import add_order
from bittrade_binance_websocket.events.cancel_order import cancel_order
from bittrade_binance_websocket.framework.framework import get_framework
from bittrade_binance_websocket.messages.listen import filter_new_socket_only
from bittrade_binance_websocket.models.order import (
    OrderCancelRequest,
    OrderResponseType,
    OrderSide,
    OrderTimeInForceType,
    MarginSymbolOrdersRequest,
    OrderType,
    PlaceOrderRequest,
    PlaceOrderResponse,
    SymbolOrdersCancelRequest,
)
from bittrade_binance_websocket.models.response_message import ResponseMessage
from IPython.terminal import embed

from bittrade_binance_websocket.rest.symbol_orders_cancel import (
    accept_empty_orders_list,
)
from bittrade_binance_websocket.sign import sign_request_factory


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


framework = get_framework(
    spot_trade_signer=add_keys,
    spot_trade_signer_http=sign_request_factory(key, secret),
    load_markets=False,
)
framework.spot_trade_socket_messages.subscribe(print, print, print)
# framework.spot_symbol_orders_cancel_http(
#     SymbolOrdersCancelRequest(symbol="BTCUSDT")
# ).pipe(accept_empty_orders_list()).subscribe(print, print, print)

# framework.spot_current_open_orders_http(SymbolOrdersCancelRequest("BTCUSDT")).subscribe(
#     print, print, print
# )
framework.margin_current_open_orders_http(
    MarginSymbolOrdersRequest(symbol="BTCUSDT", isIsolated=True)
).subscribe(print, print, print)

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
