from datetime import datetime
import os
from typing import Literal
from urllib.parse import urlencode
import hmac
import hashlib
import base64
from expression import pipe
from reactivex import Observable, concat, throw, empty, timer, just, operators, compose
import requests

from elm_framework_helpers.output import debug_operator

from bittrade_binance_websocket.sign import del_none


def sign_request_factory(key: str, secret: str):
    def hashing(query_string):
        return hmac.new(
            secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def sign(request):
        request.headers.update({"X-MBX-APIKEY": key})
        payload = del_none(request.data)
        # Code adapted from https://github.com/binance/binance-signature-examples/blob/master/python/spot/spot.py
        query_string = urlencode(payload, True)
        ts = int(datetime.now().timestamp() * 1000)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, ts)
        else:
            query_string = "timestamp={}".format(ts)

        url = request.url + "?" + query_string + "&signature=" + hashing(query_string)
        request.data = {}
        request.url = url
        return request

    return sign


def add_api_key_factory(key: str = ""):
    def _add_api_key(request: requests.models.Request):
        request.headers.update({"X-MBX-APIKEY": key})
        return request

    return _add_api_key
