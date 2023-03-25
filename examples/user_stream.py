import time
from bittrade_binance_websocket.rest import listen_key
from elm_framework_helpers.config import read_config
from bittrade_binance_websocket.connection.private_user_stream import (
    private_websocket_user_stream,
)
from bittrade_binance_websocket.framework import get_framework
from .sign import add_api_key_factory
import logging

logging.basicConfig(level=logging.DEBUG)

# make sure api key env variable is set before running this example
key = read_config("key")
signer = add_api_key_factory(key)

context = get_framework(user_stream_signer_http=signer, load_markets=False)

context.user_data_stream_messages.subscribe(print, print, print)
context.user_data_stream_sockets.subscribe(print, print, print)

context.user_data_stream_socket_bundles.connect()

time.sleep(5)

# Uncomment to see the reconnect behavior, key can be read from logs when initially connecting
# key = ""
# context.delete_listen_key_http(key).subscribe(print, print, print)

time.sleep(60)
