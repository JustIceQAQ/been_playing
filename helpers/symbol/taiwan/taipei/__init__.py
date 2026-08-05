from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TaipeiCity(Enum):
    CITY = Name(name="臺北市", code="63000000", ios3166ma=ISO3166Ma.TAIPEI_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def songshan_63000010(self) -> Location:
        return Location(city=self.value, area=Name(name="松山區", code="63000010"))

    @property
    def xinyi_63000020(self) -> Location:
        return Location(city=self.value, area=Name(name="信義區", code="63000020"))

    @property
    def daan_63000030(self) -> Location:
        return Location(city=self.value, area=Name(name="大安區", code="63000030"))

    @property
    def zhongshan_63000040(self) -> Location:
        return Location(city=self.value, area=Name(name="中山區", code="63000040"))

    @property
    def zhongzheng_63000050(self) -> Location:
        return Location(city=self.value, area=Name(name="中正區", code="63000050"))

    @property
    def datong_63000060(self) -> Location:
        return Location(city=self.value, area=Name(name="大同區", code="63000060"))

    @property
    def wanhua_63000070(self) -> Location:
        return Location(city=self.value, area=Name(name="萬華區", code="63000070"))

    @property
    def wenshan_63000080(self) -> Location:
        return Location(city=self.value, area=Name(name="文山區", code="63000080"))

    @property
    def nangang_63000090(self) -> Location:
        return Location(city=self.value, area=Name(name="南港區", code="63000090"))

    @property
    def neihu_63000100(self) -> Location:
        return Location(city=self.value, area=Name(name="內湖區", code="63000100"))

    @property
    def shilin_63000110(self) -> Location:
        return Location(city=self.value, area=Name(name="士林區", code="63000110"))

    @property
    def beitou_63000120(self) -> Location:
        return Location(city=self.value, area=Name(name="北投區", code="63000120"))
