from typing import TypedDict


class UserAsset(TypedDict):
    asset: str
    borrowed: str
    free: str
    interest: str
    locked: str
    netAsset: str


class AccountInfo(TypedDict):
    borrowEnabled: bool
    marginLevel: str
    totalAssetOfBtc: str
    totalLiabilityOfBtc: str
    totalNetAssetOfBtc: str
    tradeEnabled: bool
    transferEnabled: bool
    userAssets: list[UserAsset]
