from typing import Any, Callable, Dict, List
from reactivex import Observable, compose
from bittrade_binance_websocket.channels.subscribe import subscribe_to_channel

from bittrade_binance_websocket.models import response_message
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket

def extract_data():
    def _extract(message: Dict):
      return message

    return _extract

def subscribe_depth(
    messages: Observable[Dict | List],
    symbol: str,
) -> Callable[[Observable[EnhancedWebsocket]], Observable[Any]]:
    """Unparsed orders (only extracted result array)"""
    ticker = f'{symbol}@depth'
    return compose(
        subscribe_to_channel(messages, ticker),
        extract_data(),  # type: ignore
    )


__all__ = ["subscribe_depth"]