import os
from reactivex.testing import ReactiveTest, TestScheduler
import requests
from bittrade_binance_websocket.rest.listen_key import get_listen_key_http_factory


def test_get_listen_key():
    scheduler = TestScheduler()
    get_listen_key = get_listen_key_http_factory(lambda x: x)
    result = scheduler.start(get_listen_key)

    assert result.messages == [
        ReactiveTest.on_error(
            ticks=200,
            error=requests.HTTPError(
                "401 Client Error: Unauthorized for url: https://api.binance.com/api/v3/userDataStream"
            ),
        )
    ]
