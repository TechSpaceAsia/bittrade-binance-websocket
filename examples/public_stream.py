import logging
import time
from rich.logging import RichHandler
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.output import debug_observer, debug_operator, info_observer
from ccxt import binance
from reactivex import operators
from bittrade_binance_websocket.channels.book_ticker import parse_book_ticker_ccxt, subscribe_book_ticker
from bittrade_binance_websocket.channels.depth import parse_order_book_ccxt, subscribe_depth

from bittrade_binance_websocket.connection.public_stream import public_websocket_connection
from bittrade_binance_websocket.messages.listen import filter_new_socket_only
from bittrade_binance_websocket.channels.subscribe import subscribe_to_channel
from bittrade_binance_websocket.framework import get_framework

console = RichHandler()
console.setLevel(logging.DEBUG)  # <- if you wish to see subscribe/unsubscribe and raw messages, change to DEBUG
logger = logging.getLogger(
    'bittrade_binance_websocket'
)
logger.setLevel(logging.INFO)
logger.addHandler(console)

exchange = binance()
exchange.load_markets()
# socket_connection = public_websocket_connection()

# messages = socket_connection.pipe(
#     connection_operators.keep_messages_only(),
#     operators.share()  # Usually best to share messages to avoid overhead
# )
# messages.subscribe(info_observer('ALL MESSAGES', 'bittrade_binance_websocket'))
# Subscribe to multiple channels only when socket connects
# ready = socket_connection.pipe(
#     filter_new_socket_only(),
#     operators.share()
# )
# subscribe_to_channel gives an observable with only the messages from that channel
# ready.pipe(
#     subscribe_depth(messages, 'bnbbtc'),
#     operators.map(parse_order_book_ccxt(binance()))
# ).subscribe(
#     info_observer('TICKER bnbbtc', 'bittrade_binance_websocket')
# )

# ready.pipe(
#     subscribe_book_ticker(messages, 'bnbbtc'),
# ).subscribe(
#     info_observer('BOOKTICKER bnbbtc', 'bittrade_binance_websocket')
# )

# sub = socket_connection.connect()
framework = get_framework()
public_messages = framework.public_stream_sockets.pipe(
    operators.do_action(print, print, print),
    # subscribe_to_channel(framework.public_stream_socket_messages, f"fdusdusdt@bookTicker")
    subscribe_to_channel(framework.public_stream_socket_messages, f"usdcusdt@kline_1s")
)
framework.public_stream_bundles.connect()

# sub = public_messages.subscribe(
#     info_observer('TICKER FDUSDUSDT', 'bittrade_binance_websocket')
# )
sub = public_messages.subscribe(
    info_observer('AVG USDCUSDT', 'bittrade_binance_websocket')
)

time.sleep(30)
assert sub is not None
sub.dispose() 