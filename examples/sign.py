import os
from typing import Literal
import urllib.parse
import hmac
from urllib import parse
import hashlib
import base64
from urllib.parse import urlencode, urlparse
from reactivex import Observable, concat, throw, empty, timer, just, operators, compose
import requests

from elm_framework_helpers.output import debug_operator


def build_token_factory(key: str, secret: str):
    pass


def add_token_factory(key: str, secret: str):
    signer = build_token_factory(key, secret)


def add_api_key_factory(key: str = ""):
    def _add_api_key(request: requests.models.Request):
        request.headers.update({"X-MBX-APIKEY": key})
        return request

    return _add_api_key
