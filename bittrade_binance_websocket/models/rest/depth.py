import dataclasses
from typing import List, Tuple, TypedDict


class Depth(TypedDict):
    lastUpdatedId: int
    bids: List[Tuple[str, str]]
    asks: List[Tuple[str, str]]


@dataclasses.dataclass
class DepthRequest():
    symbol: str
    # Default 100; max 5000.
    # If limit > 5000. then the response will truncate to 5000.
    limit: int

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        return as_dict
