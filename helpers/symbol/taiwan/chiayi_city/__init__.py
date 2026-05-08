from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class ChaiyiCity(Enum):
    CITY = Name(name="嘉義市", code="10020000", ios3166ma=ISO3166Ma.CHIAYI_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def east_10020010(self) -> Location:
        return Location(city=self.value, area=Name(name="東區", code="10020010"))

    @property
    def west_10020020(self) -> Location:
        return Location(city=self.value, area=Name(name="西區", code="10020020"))
