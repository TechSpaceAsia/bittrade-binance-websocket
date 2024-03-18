from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class AccountType(Enum):
    SPOT = "SPOT"
    MARGIN = "MARGIN"
    ISOLATED_MARGIN = "ISOLATED_MARGIN"
    COIN_FUTURE = "COIN_FUTURE"
    USDT_FUTURE = "USDT_FUTURE"


@dataclass
class UniversalTransferRequest:
    from_email: str
    to_email: str
    from_account_type: AccountType
    to_account_type: AccountType
    asset: str
    amount: str
    transaction_id: str = ""
    symbol: str = ""

    def to_dict(self):
        data = {
            "fromEmail": self.from_email,
            "toEmail": self.to_email,
            "fromAccountType": self.from_account_type.value,
            "toAccountType": self.to_account_type.value,
            "asset": self.asset,
            "amount": self.amount,
            "transactionId": self.transaction_id,
            "symbol": self.symbol,
        }
        if self.symbol == "":
            del data["symbol"]
        if self.transaction_id == "":
            del data["transactionId"]
        if self.from_email == "":
            del data["fromEmail"]
        if self.to_email == "":
            del data["toEmail"]
        return data
    


