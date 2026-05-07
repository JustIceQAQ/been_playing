from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class PingtungCounty(Enum):
    CITY = Name(name="屏東縣", code="10013000", ios3166ma=ISO3166Ma.PINGTUNG_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def ping_dong_10013010(self) -> Location:
        return Location(city=self.value, area=Name(name="屏東市", code="10013010"))

    @property
    def chao_zhou_10013020(self) -> Location:
        return Location(city=self.value, area=Name(name="潮州鎮", code="10013020"))

    @property
    def dong_gang_10013030(self) -> Location:
        return Location(city=self.value, area=Name(name="東港鎮", code="10013030"))

    @property
    def heng_chun_10013040(self) -> Location:
        return Location(city=self.value, area=Name(name="恆春鎮", code="10013040"))

    @property
    def wan_dan_10013050(self) -> Location:
        return Location(city=self.value, area=Name(name="萬丹鄉", code="10013050"))

    @property
    def chang_zhi_10013060(self) -> Location:
        return Location(city=self.value, area=Name(name="長治鄉", code="10013060"))

    @property
    def lin_luo_10013070(self) -> Location:
        return Location(city=self.value, area=Name(name="麟洛鄉", code="10013070"))

    @property
    def jiu_ru_10013080(self) -> Location:
        return Location(city=self.value, area=Name(name="九如鄉", code="10013080"))

    @property
    def li_gang_10013090(self) -> Location:
        return Location(city=self.value, area=Name(name="里港鄉", code="10013090"))

    @property
    def yan_pu_10013100(self) -> Location:
        return Location(city=self.value, area=Name(name="鹽埔鄉", code="10013100"))

    @property
    def gao_shu_10013110(self) -> Location:
        return Location(city=self.value, area=Name(name="高樹鄉", code="10013110"))

    @property
    def wan_luan_10013120(self) -> Location:
        return Location(city=self.value, area=Name(name="萬巒鄉", code="10013120"))

    @property
    def nei_pu_10013130(self) -> Location:
        return Location(city=self.value, area=Name(name="內埔鄉", code="10013130"))

    @property
    def zhu_tian_10013140(self) -> Location:
        return Location(city=self.value, area=Name(name="竹田鄉", code="10013140"))

    @property
    def xin_pi_10013150(self) -> Location:
        return Location(city=self.value, area=Name(name="新埤鄉", code="10013150"))

    @property
    def fang_liao_10013160(self) -> Location:
        return Location(city=self.value, area=Name(name="枋寮鄉", code="10013160"))

    @property
    def xin_yuan_10013170(self) -> Location:
        return Location(city=self.value, area=Name(name="新園鄉", code="10013170"))

    @property
    def kan_ding_10013180(self) -> Location:
        return Location(city=self.value, area=Name(name="崁頂鄉", code="10013180"))

    @property
    def lin_bian_10013190(self) -> Location:
        return Location(city=self.value, area=Name(name="林邊鄉", code="10013190"))

    @property
    def nan_zhou_10013200(self) -> Location:
        return Location(city=self.value, area=Name(name="南州鄉", code="10013200"))

    @property
    def jia_dong_10013210(self) -> Location:
        return Location(city=self.value, area=Name(name="佳冬鄉", code="10013210"))

    @property
    def liu_qiu_10013220(self) -> Location:
        return Location(city=self.value, area=Name(name="琉球鄉", code="10013220"))

    @property
    def che_cheng_10013230(self) -> Location:
        return Location(city=self.value, area=Name(name="車城鄉", code="10013230"))

    @property
    def man_zhou_10013240(self) -> Location:
        return Location(city=self.value, area=Name(name="滿州鄉", code="10013240"))

    @property
    def fang_shan_10013250(self) -> Location:
        return Location(city=self.value, area=Name(name="枋山鄉", code="10013250"))

    @property
    def san_di_men_10013260(self) -> Location:
        return Location(city=self.value, area=Name(name="三地門鄉", code="10013260"))

    @property
    def wu_tai_10013270(self) -> Location:
        return Location(city=self.value, area=Name(name="霧台鄉", code="10013270"))

    @property
    def ma_jia_10013280(self) -> Location:
        return Location(city=self.value, area=Name(name="瑪家鄉", code="10013280"))

    @property
    def tai_wu_10013290(self) -> Location:
        return Location(city=self.value, area=Name(name="泰武鄉", code="10013290"))

    @property
    def lai_yi_10013300(self) -> Location:
        return Location(city=self.value, area=Name(name="來義鄉", code="10013300"))

    @property
    def chun_ri_10013310(self) -> Location:
        return Location(city=self.value, area=Name(name="春日鄉", code="10013310"))

    @property
    def shi_zi_10013320(self) -> Location:
        return Location(city=self.value, area=Name(name="獅子鄉", code="10013320"))

    @property
    def mu_dan_10013330(self) -> Location:
        return Location(city=self.value, area=Name(name="牡丹鄉", code="10013330"))
