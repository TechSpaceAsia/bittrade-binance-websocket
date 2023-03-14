import hashlib
import hmac
from typing import Any, Dict, Tuple
from urllib.parse import urlencode


def to_sorted_qs(values: Dict[str, Any]) -> Tuple[Tuple[str, Any]]:
    """
    Returns a tuple of sorted key-value pairs from the given dictionary.

    Args:
    - values: A dictionary containing key-value pairs.

    Returns:
    - A tuple of sorted key-value pairs, where each pair is represented as a tuple of two elements,
    the first being the key and the second being the corresponding value.
    """
    sorted_tuple = tuple()
    keys = sorted(values)
    for key in keys:
        sorted_tuple = sorted_tuple + ((key, values[key],),)

    return sorted_tuple

def encode_query_string(params: Tuple):
    """
    Returns the URL-encoded string representation of the given tuple of key-value pairs.

    Args:
    - params: A tuple of key-value pairs.

    Returns:
    - The URL-encoded string representation of the given tuple of key-value pairs.
    """
    return urlencode(params)

def get_signature(qs: str, secret: str):
    """
    Returns the SHA-256 HMAC signature of the given query string using the provided secret key.

    Args:
    - qs: The query string to sign.
    - secret: The secret key to use for signing.

    Returns:
    - The SHA-256 HMAC signature of the given query string using the provided secret key.
    """
    signed = hmac.new(secret.encode('utf-8'), qs.encode('utf-8'), hashlib.sha256)
    return signed.hexdigest()