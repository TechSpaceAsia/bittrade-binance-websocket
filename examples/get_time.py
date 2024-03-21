from bittrade_binance_websocket.rest import get_time
from IPython.terminal import embed

result = get_time.get_time_http().run()
print(result)
embed.embed()
