from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class PingtungCounty(Enum):
    CITY = Name(name="屏東縣", code="10013000", ios3166ma=ISO3166Ma.PINGTUNG_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def pingtung_10013010(self) -> Location:
        return Location(city=self.value, area=Name(name="屏東市", code="10013010"))

    @property
    def chaozhou_10013020(self) -> Location:
        return Location(city=self.value, area=Name(name="潮州鎮", code="10013020"))

    @property
    def donggang_10013030(self) -> Location:
        return Location(city=self.value, area=Name(name="東港鎮", code="10013030"))

    @property
    def hengchun_10013040(self) -> Location:
        return Location(city=self.value, area=Name(name="恆春鎮", code="10013040"))

    @property
    def wandan_10013050(self) -> Location:
        return Location(city=self.value, area=Name(name="萬丹鄉", code="10013050"))

    @property
    def changzhi_10013060(self) -> Location:
        return Location(city=self.value, area=Name(name="長治鄉", code="10013060"))

    @property
    def linluo_10013070(self) -> Location:
        return Location(city=self.value, area=Name(name="麟洛鄉", code="10013070"))

    @property
    def jiuru_10013080(self) -> Location:
        return Location(city=self.value, area=Name(name="九如鄉", code="10013080"))

    @property
    def ligang_10013090(self) -> Location:
        return Location(city=self.value, area=Name(name="里港鄉", code="10013090"))

    @property
    def yanpu_10013100(self) -> Location:
        return Location(city=self.value, area=Name(name="鹽埔鄉", code="10013100"))

    @property
    def gaoshu_10013110(self) -> Location:
        return Location(city=self.value, area=Name(name="高樹鄉", code="10013110"))

    @property
    def wanluan_10013120(self) -> Location:
        return Location(city=self.value, area=Name(name="萬巒鄉", code="10013120"))

    @property
    def neipu_10013130(self) -> Location:
        return Location(city=self.value, area=Name(name="內埔鄉", code="10013130"))

    @property
    def zhutian_10013140(self) -> Location:
        return Location(city=self.value, area=Name(name="竹田鄉", code="10013140"))

    @property
    def xinpi_10013150(self) -> Location:
        return Location(city=self.value, area=Name(name="新埤鄉", code="10013150"))

    @property
    def fangliao_10013160(self) -> Location:
        return Location(city=self.value, area=Name(name="枋寮鄉", code="10013160"))

    @property
    def xinyuan_10013170(self) -> Location:
        return Location(city=self.value, area=Name(name="新園鄉", code="10013170"))

    @property
    def kanding_10013180(self) -> Location:
        return Location(city=self.value, area=Name(name="崁頂鄉", code="10013180"))

    @property
    def linbian_10013190(self) -> Location:
        return Location(city=self.value, area=Name(name="林邊鄉", code="10013190"))

    @property
    def nanzhou_10013200(self) -> Location:
        return Location(city=self.value, area=Name(name="南州鄉", code="10013200"))

    @property
    def jiadong_10013210(self) -> Location:
        return Location(city=self.value, area=Name(name="佳冬鄉", code="10013210"))

    @property
    def liuqiu_10013220(self) -> Location:
        return Location(city=self.value, area=Name(name="琉球鄉", code="10013220"))

    @property
    def checheng_10013230(self) -> Location:
        return Location(city=self.value, area=Name(name="車城鄉", code="10013230"))

    @property
    def manzhou_10013240(self) -> Location:
        return Location(city=self.value, area=Name(name="滿州鄉", code="10013240"))

    @property
    def fangshan_10013250(self) -> Location:
        return Location(city=self.value, area=Name(name="枋山鄉", code="10013250"))

    @property
    def sandimen_10013260(self) -> Location:
        return Location(city=self.value, area=Name(name="三地門鄉", code="10013260"))

    @property
    def wutai_10013270(self) -> Location:
        return Location(city=self.value, area=Name(name="霧台鄉", code="10013270"))

    @property
    def majia_10013280(self) -> Location:
        return Location(city=self.value, area=Name(name="瑪家鄉", code="10013280"))

    @property
    def taiwu_10013290(self) -> Location:
        return Location(city=self.value, area=Name(name="泰武鄉", code="10013290"))

    @property
    def laiyi_10013300(self) -> Location:
        return Location(city=self.value, area=Name(name="來義鄉", code="10013300"))

    @property
    def chunri_10013310(self) -> Location:
        return Location(city=self.value, area=Name(name="春日鄉", code="10013310"))

    @property
    def shizi_10013320(self) -> Location:
        return Location(city=self.value, area=Name(name="獅子鄉", code="10013320"))

    @property
    def mudan_10013330(self) -> Location:
        return Location(city=self.value, area=Name(name="牡丹鄉", code="10013330"))
