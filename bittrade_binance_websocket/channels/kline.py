# @bookTicker
from typing import Any, Callable, Dict, List, cast
from reactivex import Observable, compose, operators
from ccxt import binance
from bittrade_binance_websocket.channels.subscribe import subscribe_to_channel

from bittrade_binance_websocket.models import response_message
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_binance_websocket.models.message import UserFeedMessage


def is_kline_message(x: UserFeedMessage) -> bool:
    return x.get("e", "") == "kline"


def get_kline_message(x: UserFeedMessage) -> UserFeedMessage:
    return x.get("k", {})


def subscribe_kline(
    messages: Observable[Dict | List],
    symbol: str,
    interval: str = "1d",
) -> Callable[[Observable[EnhancedWebsocket]], Observable[UserFeedMessage]]:
    """Unparsed orders (only extracted result array)"""
    ticker = f"{symbol}@kline_{interval}"
    return compose(
        subscribe_to_channel(messages, ticker),
        operators.filter(is_kline_message),
        operators.map(get_kline_message),
    )


__all__ = ["subscribe_kline"]
