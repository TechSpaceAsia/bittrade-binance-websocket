from bittrade_binance_websocket.rest import get_time

result = get_time.get_time_http().run()
print(result)
