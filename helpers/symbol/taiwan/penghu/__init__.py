from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class PenghuCounty(Enum):
    CITY = Name(name="澎湖縣", code="10016000", ios3166ma=ISO3166Ma.PENGHU_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def magong_10016010(self) -> Location:
        return Location(city=self.value, area=Name(name="馬公市", code="10016010"))

    @property
    def huxi_10016020(self) -> Location:
        return Location(city=self.value, area=Name(name="湖西鄉", code="10016020"))

    @property
    def baisha_10016030(self) -> Location:
        return Location(city=self.value, area=Name(name="白沙鄉", code="10016030"))

    @property
    def xiyu_10016040(self) -> Location:
        return Location(city=self.value, area=Name(name="西嶼鄉", code="10016040"))

    @property
    def wangan_10016050(self) -> Location:
        return Location(city=self.value, area=Name(name="望安鄉", code="10016050"))

    @property
    def qimei_10016060(self) -> Location:
        return Location(city=self.value, area=Name(name="七美鄉", code="10016060"))
