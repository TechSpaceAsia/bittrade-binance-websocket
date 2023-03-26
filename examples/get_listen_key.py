from bittrade_binance_websocket.rest import listen_key
from elm_framework_helpers.config import read_config
from .sign import add_api_key_factory

# make sure api key env variable is set before running this example
key = read_config("key")
signer = add_api_key_factory(key)
get_listen_key = listen_key.get_listen_key_http_factory(signer)
result = get_listen_key().run()
print(result)

ping_result = listen_key.ping_listen_key_http_factory(signer)(
    result.get("listenKey")
).run()
print(ping_result)

close_result = listen_key.delete_listen_key_http_factory(signer)(
    result.get("listenKey")
).run()
print(close_result)

isolated_margin_get_listen_key = listen_key.isolated_margin_get_listen_key_http_factory(
    signer
)
result = isolated_margin_get_listen_key("BTCUSDT").run()
print(result)
