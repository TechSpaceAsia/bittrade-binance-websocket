from datetime import datetime
from typing import Any, Callable
from uuid import uuid4
from elm_framework_helpers.websockets import models
import orjson
from bittrade_binance_websocket.sign import (
    encode_query_string,
    get_signature,
    to_sorted_qs,
)
from expression.core import pipe


def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # For Python 3, write `list(d.items())`; `d.items()` won’t work
    # For Python 2, write `d.items()`; `d.iteritems()` won’t work
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d


class EnhancedWebsocket(models.EnhancedWebsocket):
    key: str
    secret: str

    def get_timestamp(self) -> str:
        return str(int(datetime.now().timestamp() * 1e3))

    def send_message(self, message: Any) -> int | str:
        return self.send_json(message)

    def prepare_request(self, original_message: dict) -> tuple[str, bytes]:
        signer, get_timestamp = get_signature(self.secret), self.get_timestamp
        message = original_message.copy()
        id = message.get("id", str(uuid4()))
        message["id"] = id
        params = pipe(
            message.get("params", {}).copy(),
            del_none,
            lambda x: {**x, "apiKey": self.key, "timestamp": get_timestamp()},
            lambda x: {
                **x,
                "signature": pipe(x, to_sorted_qs, encode_query_string, signer),
            },
        )
        message["params"] = params
        return message["id"], orjson.dumps(message)
