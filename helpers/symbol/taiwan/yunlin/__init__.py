from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class YunlinCounty(Enum):
    CITY = Name(name="雲林縣", code="10009000", ios3166ma=ISO3166Ma.YUNLIN_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def dou_liu_10009010(self) -> Location:
        return Location(city=self.value, area=Name(name="斗六市", code="10009010"))

    @property
    def dou_nan_10009020(self) -> Location:
        return Location(city=self.value, area=Name(name="斗南鎮", code="10009020"))

    @property
    def hu_wei_10009030(self) -> Location:
        return Location(city=self.value, area=Name(name="虎尾鎮", code="10009030"))

    @property
    def xi_luo_10009040(self) -> Location:
        return Location(city=self.value, area=Name(name="西螺鎮", code="10009040"))

    @property
    def tu_ku_10009050(self) -> Location:
        return Location(city=self.value, area=Name(name="土庫鎮", code="10009050"))

    @property
    def bei_gang_10009060(self) -> Location:
        return Location(city=self.value, area=Name(name="北港鎮", code="10009060"))

    @property
    def gu_keng_10009070(self) -> Location:
        return Location(city=self.value, area=Name(name="古坑鄉", code="10009070"))

    @property
    def da_pi_10009080(self) -> Location:
        return Location(city=self.value, area=Name(name="大埤鄉", code="10009080"))

    @property
    def ci_tong_10009090(self) -> Location:
        return Location(city=self.value, area=Name(name="莿桐鄉", code="10009090"))

    @property
    def lin_nei_10009100(self) -> Location:
        return Location(city=self.value, area=Name(name="林內鄉", code="10009100"))

    @property
    def er_lun_10009110(self) -> Location:
        return Location(city=self.value, area=Name(name="二崙鄉", code="10009110"))

    @property
    def lun_bei_10009120(self) -> Location:
        return Location(city=self.value, area=Name(name="崙背鄉", code="10009120"))

    @property
    def mai_liao_10009130(self) -> Location:
        return Location(city=self.value, area=Name(name="麥寮鄉", code="10009130"))

    @property
    def dong_shi_10009140(self) -> Location:
        return Location(city=self.value, area=Name(name="東勢鄉", code="10009140"))

    @property
    def bao_zhong_10009150(self) -> Location:
        return Location(city=self.value, area=Name(name="褒忠鄉", code="10009150"))

    @property
    def tai_xi_10009160(self) -> Location:
        return Location(city=self.value, area=Name(name="臺西鄉", code="10009160"))

    @property
    def yuan_chang_10009170(self) -> Location:
        return Location(city=self.value, area=Name(name="元長鄉", code="10009170"))

    @property
    def si_hu_10009180(self) -> Location:
        return Location(city=self.value, area=Name(name="四湖鄉", code="10009180"))

    @property
    def kou_hu_10009190(self) -> Location:
        return Location(city=self.value, area=Name(name="口湖鄉", code="10009190"))

    @property
    def shui_lin_10009200(self) -> Location:
        return Location(city=self.value, area=Name(name="水林鄉", code="10009200"))
