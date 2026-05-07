from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TaipeiCity(Enum):
    CITY = Name(name="臺北市", code="63000000", ios3166ma=ISO3166Ma.TAIPEI_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def song_shan_63000010(self) -> Location:
        return Location(city=self.value, area=Name(name="松山區", code="63000010"))

    @property
    def xin_yi_63000020(self) -> Location:
        return Location(city=self.value, area=Name(name="信義區", code="63000020"))

    @property
    def da_an_63000030(self) -> Location:
        return Location(city=self.value, area=Name(name="大安區", code="63000030"))

    @property
    def zhong_shan_63000040(self) -> Location:
        return Location(city=self.value, area=Name(name="中山區", code="63000040"))

    @property
    def zhong_zheng_63000050(self) -> Location:
        return Location(city=self.value, area=Name(name="中正區", code="63000050"))

    @property
    def da_tong_63000060(self) -> Location:
        return Location(city=self.value, area=Name(name="大同區", code="63000060"))

    @property
    def wan_hua_63000070(self) -> Location:
        return Location(city=self.value, area=Name(name="萬華區", code="63000070"))

    @property
    def wen_shan_63000080(self) -> Location:
        return Location(city=self.value, area=Name(name="文山區", code="63000080"))

    @property
    def nan_gang_63000090(self) -> Location:
        return Location(city=self.value, area=Name(name="南港區", code="63000090"))

    @property
    def nei_hu_63000100(self) -> Location:
        return Location(city=self.value, area=Name(name="內湖區", code="63000100"))

    @property
    def shi_lin_63000110(self) -> Location:
        return Location(city=self.value, area=Name(name="士林區", code="63000110"))

    @property
    def bei_tou_63000120(self) -> Location:
        return Location(city=self.value, area=Name(name="北投區", code="63000120"))
