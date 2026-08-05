from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class HsinchuCounty(Enum):
    CITY = Name(name="新竹縣", code="10004000", ios3166ma=ISO3166Ma.HSINCHU_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def zhubei_10004010(self) -> Location:
        return Location(city=self.value, area=Name(name="竹北市", code="10004010"))

    @property
    def zhudong_10004020(self) -> Location:
        return Location(city=self.value, area=Name(name="竹東鎮", code="10004020"))

    @property
    def xinpu_10004030(self) -> Location:
        return Location(city=self.value, area=Name(name="新埔鎮", code="10004030"))

    @property
    def guanxi_10004040(self) -> Location:
        return Location(city=self.value, area=Name(name="關西鎮", code="10004040"))

    @property
    def hukou_10004050(self) -> Location:
        return Location(city=self.value, area=Name(name="湖口鄉", code="10004050"))

    @property
    def xinfeng_10004060(self) -> Location:
        return Location(city=self.value, area=Name(name="新豐鄉", code="10004060"))

    @property
    def qionglin_10004070(self) -> Location:
        return Location(city=self.value, area=Name(name="芎林鄉", code="10004070"))

    @property
    def hengshan_10004080(self) -> Location:
        return Location(city=self.value, area=Name(name="橫山鄉", code="10004080"))

    @property
    def beipu_10004090(self) -> Location:
        return Location(city=self.value, area=Name(name="北埔鄉", code="10004090"))

    @property
    def baoshan_10004100(self) -> Location:
        return Location(city=self.value, area=Name(name="寶山鄉", code="10004100"))

    @property
    def emei_10004110(self) -> Location:
        return Location(city=self.value, area=Name(name="峨眉鄉", code="10004110"))

    @property
    def jianshi_10004120(self) -> Location:
        return Location(city=self.value, area=Name(name="尖石鄉", code="10004120"))

    @property
    def wufeng_10004130(self) -> Location:
        return Location(city=self.value, area=Name(name="五峰鄉", code="10004130"))
