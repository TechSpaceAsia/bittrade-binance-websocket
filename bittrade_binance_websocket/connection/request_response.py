from typing import Callable

from reactivex import Observable, operators, disposable, abc
from bittrade_binance_websocket.models import ResponseMessage

from logging import getLogger

logger = getLogger(__name__)


def wait_for_response(
    message_id: int, sender: Observable, timeout: float = 5.0
) -> Callable[
    [Observable[ResponseMessage]], Observable[ResponseMessage]
]:
    def wait_for_response_(source: Observable[ResponseMessage]) -> Observable[ResponseMessage]:
        cached = source.pipe(
            operators.filter(lambda x: x.id == message_id),
            operators.replay(),
        )
        
        def subscribe(observer: abc.ObserverBase, scheduler: abc.SchedulerBase | None = None):
            cached_subscription = cached.connect(scheduler=scheduler)
            return disposable.CompositeDisposable(
                cached_subscription,
                sender.pipe(
                    operators.take(1),
                    operators.flat_map(lambda _: cached.pipe(
                        operators.do_action(
                            on_next=lambda x: logger.debug("[SOCKET] Received matching message %s", x)
                        ),
                    )),
                    operators.take(1),
                    operators.timeout(timeout),
                ).subscribe(observer, scheduler=scheduler)
            )
        return Observable(subscribe)
    return wait_for_response_

class RequestResponseError(Exception):
    pass


def _response_ok(response: ResponseMessage):
    if response.code > 40000:
        raise RequestResponseError(response.message)
    return response


def response_ok() -> Callable[
    [Observable[ResponseMessage]], Observable[ResponseMessage]
]:
    return operators.map(_response_ok)
