from dataclasses import dataclass
from typing import Any, Callable, Literal, NamedTuple, Optional

from ccxt import binance
from elm_framework_helpers.ccxt.models.orderbook import Orderbook
from reactivex import Observable
from reactivex.observable import ConnectableObservable
from reactivex.disposable import CompositeDisposable
from reactivex.scheduler import ThreadPoolScheduler
from elm_framework_helpers.websockets import models
from bittrade_binance_websocket.models import UserFeedMessage
from bittrade_binance_websocket.models.rest.listen_key import CreateListenKeyResponse


class BookConfig(NamedTuple):
    pair: str
    depth: int


@dataclass
class FrameworkContext:
    all_subscriptions: CompositeDisposable
    exchange: binance
    get_active_listen_key_http: Callable[[], Observable[CreateListenKeyResponse]]
    get_listen_key_http: Callable[[], Observable[CreateListenKeyResponse]]
    delete_listen_key_http: Callable[[str], Observable[None]]
    keep_alive_listen_key_http: Callable[[str], Observable[None]]
    scheduler: ThreadPoolScheduler
    user_data_stream_sockets: Observable[models.EnhancedWebsocket]
    user_data_stream_socket_bundles: ConnectableObservable[models.WebsocketBundle]
    user_data_stream_messages: Observable[UserFeedMessage]
