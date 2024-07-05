import dataclasses
from typing import Optional


@dataclasses.dataclass
class KlineRequest:
    symbol: str
    interval: str
    startTime: Optional[int]
    endTime: Optional[int]
    limit: Optional[int]
    timeZone: Optional[str]
    is_margin: Optional[bool] = False

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        del as_dict["is_margin"]
        return as_dict
