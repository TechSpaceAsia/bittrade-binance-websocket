from typing import Any, Callable, Dict, List, cast
from reactivex import Observable, compose, operators
from ccxt import binance
from bittrade_binance_websocket.channels.subscribe import subscribe_to_channel

from bittrade_binance_websocket.models import response_message
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_binance_websocket.models.message import UserFeedMessage

def extract_data():
    def _extract(message: UserFeedMessage):
        return message

    return _extract


def accumulate_book_price(acc: UserFeedMessage, current: UserFeedMessage) -> UserFeedMessage:
    # if acc["u"] < current["U"]: # type: ignore
    #     raise Exception("Invalid message order")
    
    acc["e"] = current.get("e") # type: ignore
    acc["E"] = current.get("E")  # type: ignore
    acc["s"] = current.get("s")  # type: ignore
    acc["U"] = current.get("U")  # type: ignore
    acc["u"] = current.get("u")  # type: ignore

    current_asks = current.get("a", [])
    current_bids = current.get("b", [])

    asks = acc.get("a", [])
    bids = acc.get("b", [])

    if current_asks and len(asks):
        for price in current_asks:
            for ask_index, current_price in enumerate(asks):
                if price[0] == current_price[0]:
                    if not float(price[1]):
                        asks.pop(ask_index)
                        break

                    asks[ask_index] = price
                    break

                if price[0] <= current_price[0] and float(price[1]):
                    asks.insert(ask_index, price)
                    break
    elif not len(asks):
        asks = current_asks

    if current_bids and len(bids):
        for price in current_bids:
            for bid_index, current_price in enumerate(bids):
                if price[0] == current_price[0]:
                    if not float(price[1]):
                        bids.pop(bid_index)
                        break

                    bids[bid_index] = price
                    break

                if price[0] >= current_price[0] and float(price[1]):
                    bids.insert(bid_index, price)
                    break
    elif not len(bids):
        bids = current_bids

    acc["b"] = bids # type: ignore
    acc["a"] = asks # type: ignore
    return acc


def parse_order_book_ccxt(exchange: binance):
   def _parse_order_book_ccxt(messages: UserFeedMessage):
      timestamp = messages.get('E', '')
      symbol = messages.get('s', '')
      return exchange.parse_order_book(messages, symbol, timestamp, bidsKey='b', asksKey='a')
   
   return _parse_order_book_ccxt

def subscribe_depth(
    messages: Observable[Dict | List],
    symbol: str,
    default_orderbook: UserFeedMessage,
    depth_level: int = 5,
    update_speed: int = 100
) -> Callable[[Observable[EnhancedWebsocket]], Observable[UserFeedMessage]]:
    """Unparsed orders (only extracted result array)"""
    ticker = f'{symbol}@depth'
    return compose(
        subscribe_to_channel(messages, ticker),
        operators.map(extract_data()),
        operators.scan(accumulate_book_price, default_orderbook),
    )


__all__ = ["subscribe_depth", "parse_order_book_ccxt"]
