from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class ChaiyiCounty(Enum):
    CITY = Name(name="嘉義縣", code="10010000", ios3166ma=ISO3166Ma.CHIAYI_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def taibao_10010010(self) -> Location:
        return Location(city=self.value, area=Name(name="太保市", code="10010010"))

    @property
    def puzi_10010020(self) -> Location:
        return Location(city=self.value, area=Name(name="朴子市", code="10010020"))

    @property
    def budai_10010030(self) -> Location:
        return Location(city=self.value, area=Name(name="布袋鎮", code="10010030"))

    @property
    def dalin_10010040(self) -> Location:
        return Location(city=self.value, area=Name(name="大林鎮", code="10010040"))

    @property
    def minxiong_10010050(self) -> Location:
        return Location(city=self.value, area=Name(name="民雄鄉", code="10010050"))

    @property
    def xikou_10010060(self) -> Location:
        return Location(city=self.value, area=Name(name="溪口鄉", code="10010060"))

    @property
    def xingang_10010070(self) -> Location:
        return Location(city=self.value, area=Name(name="新港鄉", code="10010070"))

    @property
    def liujiao_10010080(self) -> Location:
        return Location(city=self.value, area=Name(name="六腳鄉", code="10010080"))

    @property
    def dongshi_10010090(self) -> Location:
        return Location(city=self.value, area=Name(name="東石鄉", code="10010090"))

    @property
    def yizhu_10010100(self) -> Location:
        return Location(city=self.value, area=Name(name="義竹鄉", code="10010100"))

    @property
    def lucao_10010110(self) -> Location:
        return Location(city=self.value, area=Name(name="鹿草鄉", code="10010110"))

    @property
    def shuishang_10010120(self) -> Location:
        return Location(city=self.value, area=Name(name="水上鄉", code="10010120"))

    @property
    def zhongpu_10010130(self) -> Location:
        return Location(city=self.value, area=Name(name="中埔鄉", code="10010130"))

    @property
    def zhuqi_10010140(self) -> Location:
        return Location(city=self.value, area=Name(name="竹崎鄉", code="10010140"))

    @property
    def meishan_10010150(self) -> Location:
        return Location(city=self.value, area=Name(name="梅山鄉", code="10010150"))

    @property
    def fanlu_10010160(self) -> Location:
        return Location(city=self.value, area=Name(name="番路鄉", code="10010160"))

    @property
    def dapu_10010170(self) -> Location:
        return Location(city=self.value, area=Name(name="大埔鄉", code="10010170"))

    @property
    def alishan_10010180(self) -> Location:
        return Location(city=self.value, area=Name(name="阿里山鄉", code="10010180"))
