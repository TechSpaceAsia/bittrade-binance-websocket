from typing import Any, Callable
from reactivex import Observable, operators

from logging import getLogger
from typing import Callable, Optional, cast, TYPE_CHECKING

import requests
from ccxt import binance
from reactivex import Observable, operators
from reactivex.disposable import CompositeDisposable
from reactivex.operators import flat_map, share
from reactivex.scheduler import ThreadPoolScheduler
from reactivex.subject import BehaviorSubject
from bittrade_binance_websocket import models
from elm_framework_helpers.websockets.operators import connection_operators
from bittrade_binance_websocket.connection.private_user_stream import (
    private_websocket_user_stream,
)
from bittrade_binance_websocket.models.framework import FrameworkContext
from elm_framework_helpers.output import debug_operator

from bittrade_binance_websocket.rest.listen_key import (
    get_active_listen_key_http_factory,
    get_listen_key_http_factory,
    ping_listen_key_http_factory,
    delete_listen_key_http_factory,
)


logger = getLogger(__name__)


def get_framework(
    *,
    add_token: Callable[
        [Observable[models.ResponseMessage]],
        Callable[
            [Observable[models.EnhancedWebsocket]], Observable[models.ResponseMessage]
        ],
    ] = None,
    user_stream_signer_http: Callable[
        [requests.models.Request], requests.models.Request
    ] = None,
    user_data_signer_http: Callable[
        [requests.models.Request], requests.models.Request
    ] = None,
    load_markets=True,
) -> FrameworkContext:
    exchange = binance()
    if load_markets:
        exchange.load_markets()
    pool_scheduler = ThreadPoolScheduler(200)
    all_subscriptions = CompositeDisposable()
    # Rest
    get_active_listen_key_http = get_active_listen_key_http_factory(
        user_stream_signer_http
    )
    get_listen_key_http = get_listen_key_http_factory(user_stream_signer_http)
    keep_alive_listen_key_http = ping_listen_key_http_factory(user_stream_signer_http)
    delete_listen_key_http = delete_listen_key_http_factory(user_stream_signer_http)

    # Set up sockets
    user_data_stream_socket_bundles = private_websocket_user_stream(
        get_listen_key_http, keep_alive_listen_key_http
    )
    user_data_stream_socket = user_data_stream_socket_bundles.pipe(
        connection_operators.keep_new_socket_only()
    )

    user_data_stream_messages = user_data_stream_socket_bundles.pipe(
        connection_operators.keep_messages_only()
    )

    return FrameworkContext(
        all_subscriptions=all_subscriptions,
        exchange=exchange,
        delete_listen_key_http=delete_listen_key_http,
        get_active_listen_key_http=get_active_listen_key_http,
        get_listen_key_http=get_listen_key_http,
        keep_alive_listen_key_http=keep_alive_listen_key_http,
        user_data_stream_messages=user_data_stream_messages,
        user_data_stream_sockets=user_data_stream_socket,
        user_data_stream_socket_bundles=user_data_stream_socket_bundles,
        scheduler=pool_scheduler,
    )
