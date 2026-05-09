from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TaitungCounty(Enum):
    CITY = Name(name="臺東縣", code="10014000", ios3166ma=ISO3166Ma.TAITUNG_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def taitung_10014010(self) -> Location:
        return Location(city=self.value, area=Name(name="臺東市", code="10014010"))

    @property
    def chenggong_10014020(self) -> Location:
        return Location(city=self.value, area=Name(name="成功鎮", code="10014020"))

    @property
    def guanshan_10014030(self) -> Location:
        return Location(city=self.value, area=Name(name="關山鎮", code="10014030"))

    @property
    def beinan_10014040(self) -> Location:
        return Location(city=self.value, area=Name(name="卑南鄉", code="10014040"))

    @property
    def luye_10014050(self) -> Location:
        return Location(city=self.value, area=Name(name="鹿野鄉", code="10014050"))

    @property
    def chishang_10014060(self) -> Location:
        return Location(city=self.value, area=Name(name="池上鄉", code="10014060"))

    @property
    def donghe_10014070(self) -> Location:
        return Location(city=self.value, area=Name(name="東河鄉", code="10014070"))

    @property
    def changbin_10014080(self) -> Location:
        return Location(city=self.value, area=Name(name="長濱鄉", code="10014080"))

    @property
    def taimali_10014090(self) -> Location:
        return Location(city=self.value, area=Name(name="太麻里鄉", code="10014090"))

    @property
    def dawu_10014100(self) -> Location:
        return Location(city=self.value, area=Name(name="大武鄉", code="10014100"))

    @property
    def ludao_10014110(self) -> Location:
        return Location(city=self.value, area=Name(name="綠島鄉", code="10014110"))

    @property
    def haiduan_10014120(self) -> Location:
        return Location(city=self.value, area=Name(name="海端鄉", code="10014120"))

    @property
    def yanping_10014130(self) -> Location:
        return Location(city=self.value, area=Name(name="延平鄉", code="10014130"))

    @property
    def jinfeng_10014140(self) -> Location:
        return Location(city=self.value, area=Name(name="金峰鄉", code="10014140"))

    @property
    def daren_10014150(self) -> Location:
        return Location(city=self.value, area=Name(name="達仁鄉", code="10014150"))

    @property
    def lanyu_10014160(self) -> Location:
        return Location(city=self.value, area=Name(name="蘭嶼鄉", code="10014160"))
