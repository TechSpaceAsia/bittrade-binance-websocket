from bittrade_binance_websocket.rest import listen_key

# make sure api key env variable is set before running this example
result = listen_key.get_listen_key().run()
print(result)

ping_result = listen_key.ping_listen_key(result.get('listenKey')).run()
print(ping_result)

close_result = listen_key.close_listen_key(result.get('listenKey')).run()
print(close_result)