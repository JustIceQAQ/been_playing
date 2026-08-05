from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class KinmenCounty(Enum):
    CITY = Name(name="金門縣", code="09020000", ios3166ma=ISO3166Ma.KINMEN_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def jincheng_09020010(self) -> Location:
        return Location(city=self.value, area=Name(name="金城鎮", code="09020010"))

    @property
    def jinhu_09020020(self) -> Location:
        return Location(city=self.value, area=Name(name="金湖鎮", code="09020020"))

    @property
    def jinsha_09020030(self) -> Location:
        return Location(city=self.value, area=Name(name="金沙鎮", code="09020030"))

    @property
    def jinning_09020040(self) -> Location:
        return Location(city=self.value, area=Name(name="金寧鄉", code="09020040"))

    @property
    def lieyu_09020050(self) -> Location:
        return Location(city=self.value, area=Name(name="烈嶼鄉", code="09020050"))

    @property
    def wuqiu_09020060(self) -> Location:
        return Location(city=self.value, area=Name(name="烏坵鄉", code="09020060"))
