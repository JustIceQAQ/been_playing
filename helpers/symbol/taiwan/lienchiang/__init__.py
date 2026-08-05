from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class LienchiangCounty(Enum):
    CITY = Name(name="連江縣", code="09007000", ios3166ma=ISO3166Ma.LIENCHIANG_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def nangan_09007010(self) -> Location:
        return Location(city=self.value, area=Name(name="南竿鄉", code="09007010"))

    @property
    def beigan_09007020(self) -> Location:
        return Location(city=self.value, area=Name(name="北竿鄉", code="09007020"))

    @property
    def juguang_09007030(self) -> Location:
        return Location(city=self.value, area=Name(name="莒光鄉", code="09007030"))

    @property
    def dongyin_09007040(self) -> Location:
        return Location(city=self.value, area=Name(name="東引鄉", code="09007040"))
