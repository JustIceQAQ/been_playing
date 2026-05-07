from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class PenghuCounty(Enum):
    CITY = Name(name="澎湖縣", code="10016000", ios3166ma=ISO3166Ma.PENGHU_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def ma_gong_10016010(self) -> Location:
        return Location(city=self.value, area=Name(name="馬公市", code="10016010"))

    @property
    def hu_xi_10016020(self) -> Location:
        return Location(city=self.value, area=Name(name="湖西鄉", code="10016020"))

    @property
    def bai_sha_10016030(self) -> Location:
        return Location(city=self.value, area=Name(name="白沙鄉", code="10016030"))

    @property
    def xi_yu_10016040(self) -> Location:
        return Location(city=self.value, area=Name(name="西嶼鄉", code="10016040"))

    @property
    def wang_an_10016050(self) -> Location:
        return Location(city=self.value, area=Name(name="望安鄉", code="10016050"))

    @property
    def qi_mei_10016060(self) -> Location:
        return Location(city=self.value, area=Name(name="七美鄉", code="10016060"))
