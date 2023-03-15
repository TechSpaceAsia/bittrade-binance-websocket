from bittrade_binance_websocket.rest import listen_key

# make sure api key env variable is set before running this example
result = listen_key.get_listen_key().run()
print(result)
