from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class YilanCounty(Enum):
    CITY = Name(name="宜蘭縣", code="10002000", ios3166ma=ISO3166Ma.YILAN_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def yi_lan_10002010(self) -> Location:
        return Location(city=self.value, area=Name(name="宜蘭市", code="10002010"))

    @property
    def luo_dong_10002020(self) -> Location:
        return Location(city=self.value, area=Name(name="羅東鎮", code="10002020"))

    @property
    def su_ao_10002030(self) -> Location:
        return Location(city=self.value, area=Name(name="蘇澳鎮", code="10002030"))

    @property
    def tou_cheng_10002040(self) -> Location:
        return Location(city=self.value, area=Name(name="頭城鎮", code="10002040"))

    @property
    def jiao_xi_10002050(self) -> Location:
        return Location(city=self.value, area=Name(name="礁溪鄉", code="10002050"))

    @property
    def zhuang_wei_10002060(self) -> Location:
        return Location(city=self.value, area=Name(name="壯圍鄉", code="10002060"))

    @property
    def yuan_shan_10002070(self) -> Location:
        return Location(city=self.value, area=Name(name="員山鄉", code="10002070"))

    @property
    def dong_shan_10002080(self) -> Location:
        return Location(city=self.value, area=Name(name="冬山鄉", code="10002080"))

    @property
    def wu_jie_10002090(self) -> Location:
        return Location(city=self.value, area=Name(name="五結鄉", code="10002090"))

    @property
    def san_xing_10002100(self) -> Location:
        return Location(city=self.value, area=Name(name="三星鄉", code="10002100"))

    @property
    def da_tong_10002110(self) -> Location:
        return Location(city=self.value, area=Name(name="大同鄉", code="10002110"))

    @property
    def nan_ao_10002120(self) -> Location:
        return Location(city=self.value, area=Name(name="南澳鄉", code="10002120"))
