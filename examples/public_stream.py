import logging
import time
from rich.logging import RichHandler
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.output import debug_observer, debug_operator, info_observer
from reactivex import operators
from bittrade_binance_websocket.channels.depth import subscribe_depth

from bittrade_binance_websocket.connection.public_stream import public_websocket_connection
from bittrade_binance_websocket.messages.listen import filter_new_socket_only

console = RichHandler()
console.setLevel(logging.INFO)  # <- if you wish to see subscribe/unsubscribe and raw messages, change to DEBUG
logger = logging.getLogger(
    'bittrade_binance_websocket'
)
logger.setLevel(logging.DEBUG)
logger.addHandler(console)

socket_connection = public_websocket_connection()

messages = socket_connection.pipe(
    connection_operators.keep_messages_only(),
    operators.share()  # Usually best to share messages to avoid overhead
)
messages.subscribe(info_observer('ALL MESSAGES', 'bittrade_binance_websocket'))
# Subscribe to multiple channels only when socket connects
ready = socket_connection.pipe(
    filter_new_socket_only(),
    operators.share()
)
# subscribe_to_channel gives an observable with only the messages from that channel
ready.pipe(
    subscribe_depth(messages, 'bnbbtc')
).subscribe(
    info_observer('TICKER bnbbtc', 'bittrade_binance_websocket')
)

sub = socket_connection.connect()

time.sleep(30)
assert sub is not None
sub.dispose() 