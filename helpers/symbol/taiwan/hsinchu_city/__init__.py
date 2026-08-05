from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class HsinchuCity(Enum):
    CITY = Name(name="新竹市", code="10018000", ios3166ma=ISO3166Ma.HSINCHU_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def east_10018010(self) -> Location:
        return Location(city=self.value, area=Name(name="東區", code="10018010"))

    @property
    def north_10018020(self) -> Location:
        return Location(city=self.value, area=Name(name="北區", code="10018020"))

    @property
    def xiangshan_10018030(self) -> Location:
        return Location(city=self.value, area=Name(name="香山區", code="10018030"))
