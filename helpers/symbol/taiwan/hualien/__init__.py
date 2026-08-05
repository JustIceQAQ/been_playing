from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class HualienCounty(Enum):
    CITY = Name(name="花蓮縣", code="10015000", ios3166ma=ISO3166Ma.HUALIEN_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def hualien_10015010(self) -> Location:
        return Location(city=self.value, area=Name(name="花蓮市", code="10015010"))

    @property
    def fenglin_10015020(self) -> Location:
        return Location(city=self.value, area=Name(name="鳳林鎮", code="10015020"))

    @property
    def yuli_10015030(self) -> Location:
        return Location(city=self.value, area=Name(name="玉里鎮", code="10015030"))

    @property
    def xincheng_10015040(self) -> Location:
        return Location(city=self.value, area=Name(name="新城鄉", code="10015040"))

    @property
    def jian_10015050(self) -> Location:
        return Location(city=self.value, area=Name(name="吉安鄉", code="10015050"))

    @property
    def shoufeng_10015060(self) -> Location:
        return Location(city=self.value, area=Name(name="壽豐鄉", code="10015060"))

    @property
    def guangfu_10015070(self) -> Location:
        return Location(city=self.value, area=Name(name="光復鄉", code="10015070"))

    @property
    def fengbin_10015080(self) -> Location:
        return Location(city=self.value, area=Name(name="豐濱鄉", code="10015080"))

    @property
    def ruisui_10015090(self) -> Location:
        return Location(city=self.value, area=Name(name="瑞穗鄉", code="10015090"))

    @property
    def fuli_10015100(self) -> Location:
        return Location(city=self.value, area=Name(name="富里鄉", code="10015100"))

    @property
    def xiulin_10015110(self) -> Location:
        return Location(city=self.value, area=Name(name="秀林鄉", code="10015110"))

    @property
    def wanrong_10015120(self) -> Location:
        return Location(city=self.value, area=Name(name="萬榮鄉", code="10015120"))

    @property
    def zhuoxi_10015130(self) -> Location:
        return Location(city=self.value, area=Name(name="卓溪鄉", code="10015130"))
