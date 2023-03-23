import logging
import time
from rich.logging import RichHandler
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.output import debug_observer, debug_operator, info_observer
from ccxt import binance
from reactivex import operators
from bittrade_binance_websocket.channels.book_ticker import parse_book_ticker_ccxt, subscribe_book_ticker
from bittrade_binance_websocket.channels.depth import parse_order_book_ccxt, subscribe_depth
from bittrade_binance_websocket.connection.private import private_websocket_connection

from bittrade_binance_websocket.connection.public_stream import public_websocket_connection
from bittrade_binance_websocket.events.ping import ping
from bittrade_binance_websocket.messages.listen import filter_new_socket_only

console = RichHandler()
console.setLevel(logging.INFO)  # <- if you wish to see subscribe/unsubscribe and raw messages, change to DEBUG
logger = logging.getLogger(
    'bittrade_binance_websocket'
)
logger.setLevel(logging.DEBUG)
logger.addHandler(console)

socket_connection = private_websocket_connection()

messages = socket_connection.pipe(
    connection_operators.keep_messages_only(),
    operators.share()  # Usually best to share messages to avoid overhead
)
messages.subscribe(info_observer('ALL MESSAGES', 'bittrade_binance_websocket'))
# Subscribe to multiple channels only when socket connects
ready = socket_connection.pipe(
    filter_new_socket_only(),
    operators.replay(1),
    operators.ref_count(),
)

sub1 = ready.pipe(
    ping(messages),
).subscribe(
    info_observer('PING', 'bittrade_binance_websocket')
)

sub = socket_connection.connect()

time.sleep(3)
sub2 = ready.pipe(
    ping(messages)
).subscribe(
    info_observer('PING 2', 'bittrade_binance_websocket')
)

time.sleep(10)
assert sub is not None
sub.dispose() 
