import dataclasses
from enum import Enum
from typing import Literal, Optional, TypedDict


@dataclasses.dataclass
class AccountBorrowRequest:
    asset: str
    amount: str
    isIsolated: Optional[bool] = False
    symbol: str = ""

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        if self.isIsolated:
            as_dict["isIsolated"] = "TRUE" if self.isIsolated else "FALSE"
        else:
            del as_dict["symbol"]
        return as_dict


@dataclasses.dataclass
class MaxBorrowableRequest:
    asset: str
    isolated_symbol: str = ""

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        del as_dict["isolated_symbol"]
        if self.isolated_symbol:
            as_dict["isolatedSymbol"] = self.isolated_symbol
        return as_dict


class FutureInterestRate(TypedDict):
    asset: str
    nextHourlyInterestRate: str

class InterestHistory(TypedDict):
    txId: str
    asset: str
    interestAccuredTime: int
    rawAsset: str  # Only present if NOT isolated symbol
    principal: str
    interest: str
    interestRate: str
    type: Literal["PERIODIC", "ON_BORROW", "PERIODIC_CONVERTED", "ON_BORROW_CONVERTED", "PORTFOLIO"]
    isolatedSymbol: str  # Only present if isolated symbol

class InterestHistoryResponse(TypedDict):
    total: int
    rows: list[InterestHistory]

class BorrowRepayRecord(TypedDict):
    txId: str
    asset: str
    timestamp: int
    status: Literal["PENDING", "CONFIRMED", "FAILED"]
    amount: str
    interest: str
    principal: str
    isolatedSymbol: str  # Only present if isolated symbol

class BorrowRepayRecordResponse(TypedDict):
    total: int
    rows: list[BorrowRepayRecord]
