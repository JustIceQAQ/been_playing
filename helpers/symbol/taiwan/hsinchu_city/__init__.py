from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class HsinchuCity(Enum):
    CITY = Name(name="新竹市", code="10018000", ios3166ma=ISO3166Ma.HSINCHU_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def dong_10018010(self) -> Location:
        return Location(city=self.value, area=Name(name="東區", code="10018010"))

    @property
    def bei_10018020(self) -> Location:
        return Location(city=self.value, area=Name(name="北區", code="10018020"))

    @property
    def xiang_shan_10018030(self) -> Location:
        return Location(city=self.value, area=Name(name="香山區", code="10018030"))
