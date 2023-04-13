from datetime import datetime, timedelta
import json
import csv
import logging
from uuid import uuid4
from rich.logging import RichHandler
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.output import debug_observer, debug_operator, info_observer
from reactivex import Observable, operators
from bittrade_binance_websocket.connection.private import private_websocket_connection
from elm_framework_helpers.config import read_config

from bittrade_binance_websocket.framework.framework import get_framework
from bittrade_binance_websocket.sign import user_stream_signer_factory
from bittrade_binance_websocket.models.trade import TradeDataRequest
from IPython.terminal import embed

from bittrade_binance_websocket.rest.trade_list import (
    account_trade_list_http_factory
)
import functools
from bittrade_binance_websocket.sign import sign_request_factory


console = RichHandler()
console.setLevel(
    logging.DEBUG
)  # <- if you wish to see subscribe/unsubscribe and raw messages, change to DEBUG
logger_name = ""
logger = logging.getLogger(logger_name)
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
    user_stream_signer_http=user_stream_signer_factory(key),
    spot_trade_signer=add_keys,
    trade_signer_http=sign_request_factory(key, secret),
    load_markets=False,
)


trade_list_request = TradeDataRequest(
    symbol="BTCTUSD",
    isIsolated=False,
    is_margin=False,
    startTime=datetime.now() - timedelta(hours=32),
)

lister = account_trade_list_http_factory(sign_request_factory(key, secret))

def write_to_csv(x):
    keys = ['symbol',
 'id',
 'orderId',
 'orderListId',
 'price',
 'qty',
 'quoteQty',
 'commission',
 'commissionAsset',
 'time',
 'isBuyer',
 'isMaker',
 'isBestMatch']
    with open('data.json', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for d in x:
            writer.writerow([d.get(k, '') for k in keys])
    print('DONE WRITING')

lister(trade_list_request).pipe(operators.reduce(lambda acc, curr: acc + curr, [])).subscribe(write_to_csv)

embed.embed()

