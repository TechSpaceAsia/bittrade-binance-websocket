from datetime import datetime
from typing import Any, Callable, Literal, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import loan

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(Any)
def available_inventory_http_factory(
    is_isolated: Optional[bool] = False,
):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_AVAILABLE_INVENTORY,
        params={"type": "MARGIN" if not is_isolated else "ISOLATED"},
    )

@http_factory(loan.AccountBorrowRequest)
def account_borrow_http_factory(
    params: loan.AccountBorrowRequest,
):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.MARGIN_LOAN,
        params=params.to_dict(),
    )


@http_factory(loan.AccountBorrowRequest)
def account_repay_http_factory(
    params: loan.AccountBorrowRequest,
):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.MARGIN_REPAY,
        params=params.to_dict(),
    )


@http_factory(loan.MaxBorrowableRequest)
def max_borrowable_http_factory(
    params: loan.MaxBorrowableRequest,
):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_MAX_BORROWABLE,
        params=params.to_dict(),
    )

@http_factory(list[loan.FutureInterestRate])
def future_hourly_interest_rate_http_factory(assets: list[str], is_isolated=False):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_FUTURE_INTEREST_RATE,
        params={
            "assets": ",".join(assets),
            "isIsolated": "TRUE" if is_isolated else "FALSE"
        },
    )

@http_factory(list[loan.InterestHistoryResponse])
def interest_history_http_factory(asset: str, isolated_symbol: Optional[str]="", size: Optional[int]=100, current_page: Optional[int]=1):
    params: dict = {
        "size": size,
        "current": current_page
    }
    if asset:
        params["asset"] = asset
    if isolated_symbol:
        params["isolatedSymbol"] = isolated_symbol
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_INTEREST_HISTORY,
        params=params,
    )

@http_factory(list[loan.BorrowRepayRecordResponse])
def query_borrow_repay_http_factory(asset: str, type: Literal["BORROW", "REPAY"], isolated_symbol: Optional[str]="", size: Optional[int]=10, current_page: Optional[int]=1, start_time: Optional[datetime]=None, end_time: Optional[datetime]=None):
    # Note that you may pass an empty string for asset to retrieve all entries, but that is discouraged.
    params = {
        "size": size,
        "current": current_page,
        "type": type
    }
    if asset:
        params["asset"] = asset
    if start_time:
        params["startTime"] = int(start_time.timestamp() * 1000)
    if end_time:
        params["endTime"] = int(end_time.timestamp() * 1000)
    if isolated_symbol:
        params["isolatedSymbol"] = isolated_symbol
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_QUERY_BORROW_REPAY_RECORDS,
        params=params,
    )
