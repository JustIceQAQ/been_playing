from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class MiaoliCounty(Enum):
    CITY = Name(name="苗栗縣", code="10005000", ios3166ma=ISO3166Ma.MIAOLI_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def miaoli_10005010(self) -> Location:
        return Location(city=self.value, area=Name(name="苗栗市", code="10005010"))

    @property
    def yuanli_10005020(self) -> Location:
        return Location(city=self.value, area=Name(name="苑裡鎮", code="10005020"))

    @property
    def tongxiao_10005030(self) -> Location:
        return Location(city=self.value, area=Name(name="通霄鎮", code="10005030"))

    @property
    def zhunan_10005040(self) -> Location:
        return Location(city=self.value, area=Name(name="竹南鎮", code="10005040"))

    @property
    def toufen_10005050(self) -> Location:
        return Location(city=self.value, area=Name(name="頭份市", code="10005050"))

    @property
    def houlong_10005060(self) -> Location:
        return Location(city=self.value, area=Name(name="後龍鎮", code="10005060"))

    @property
    def zhuolan_10005070(self) -> Location:
        return Location(city=self.value, area=Name(name="卓蘭鎮", code="10005070"))

    @property
    def dahu_10005080(self) -> Location:
        return Location(city=self.value, area=Name(name="大湖鄉", code="10005080"))

    @property
    def gongguan_10005090(self) -> Location:
        return Location(city=self.value, area=Name(name="公館鄉", code="10005090"))

    @property
    def tongluo_10005100(self) -> Location:
        return Location(city=self.value, area=Name(name="銅鑼鄉", code="10005100"))

    @property
    def nanzhuang_10005110(self) -> Location:
        return Location(city=self.value, area=Name(name="南庄鄉", code="10005110"))

    @property
    def touwu_10005120(self) -> Location:
        return Location(city=self.value, area=Name(name="頭屋鄉", code="10005120"))

    @property
    def sanyi_10005130(self) -> Location:
        return Location(city=self.value, area=Name(name="三義鄉", code="10005130"))

    @property
    def xihu_10005140(self) -> Location:
        return Location(city=self.value, area=Name(name="西湖鄉", code="10005140"))

    @property
    def zaoqiao_10005150(self) -> Location:
        return Location(city=self.value, area=Name(name="造橋鄉", code="10005150"))

    @property
    def sanwan_10005160(self) -> Location:
        return Location(city=self.value, area=Name(name="三灣鄉", code="10005160"))

    @property
    def shitan_10005170(self) -> Location:
        return Location(city=self.value, area=Name(name="獅潭鄉", code="10005170"))

    @property
    def taian_10005180(self) -> Location:
        return Location(city=self.value, area=Name(name="泰安鄉", code="10005180"))
