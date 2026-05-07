from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class ChanghuaCounty(Enum):
    CITY = Name(name="彰化縣", code="10007000", ios3166ma=ISO3166Ma.CHANGHUA_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def zhang_hua_10007010(self) -> Location:
        return Location(city=self.value, area=Name(name="彰化市", code="10007010"))

    @property
    def lu_gang_10007020(self) -> Location:
        return Location(city=self.value, area=Name(name="鹿港鎮", code="10007020"))

    @property
    def he_mei_10007030(self) -> Location:
        return Location(city=self.value, area=Name(name="和美鎮", code="10007030"))

    @property
    def xian_xi_10007040(self) -> Location:
        return Location(city=self.value, area=Name(name="線西鄉", code="10007040"))

    @property
    def shen_gang_10007050(self) -> Location:
        return Location(city=self.value, area=Name(name="伸港鄉", code="10007050"))

    @property
    def fu_xing_10007060(self) -> Location:
        return Location(city=self.value, area=Name(name="福興鄉", code="10007060"))

    @property
    def xiu_shui_10007070(self) -> Location:
        return Location(city=self.value, area=Name(name="秀水鄉", code="10007070"))

    @property
    def hua_tan_10007080(self) -> Location:
        return Location(city=self.value, area=Name(name="花壇鄉", code="10007080"))

    @property
    def fen_yuan_10007090(self) -> Location:
        return Location(city=self.value, area=Name(name="芬園鄉", code="10007090"))

    @property
    def yuan_lin_10007100(self) -> Location:
        return Location(city=self.value, area=Name(name="員林市", code="10007100"))

    @property
    def xi_hu_10007110(self) -> Location:
        return Location(city=self.value, area=Name(name="溪湖鎮", code="10007110"))

    @property
    def tian_zhong_10007120(self) -> Location:
        return Location(city=self.value, area=Name(name="田中鎮", code="10007120"))

    @property
    def da_cun_10007130(self) -> Location:
        return Location(city=self.value, area=Name(name="大村鄉", code="10007130"))

    @property
    def pu_yan_10007140(self) -> Location:
        return Location(city=self.value, area=Name(name="埔鹽鄉", code="10007140"))

    @property
    def pu_xin_10007150(self) -> Location:
        return Location(city=self.value, area=Name(name="埔心鄉", code="10007150"))

    @property
    def yong_jing_10007160(self) -> Location:
        return Location(city=self.value, area=Name(name="永靖鄉", code="10007160"))

    @property
    def she_tou_10007170(self) -> Location:
        return Location(city=self.value, area=Name(name="社頭鄉", code="10007170"))

    @property
    def er_shui_10007180(self) -> Location:
        return Location(city=self.value, area=Name(name="二水鄉", code="10007180"))

    @property
    def bei_dou_10007190(self) -> Location:
        return Location(city=self.value, area=Name(name="北斗鎮", code="10007190"))

    @property
    def er_lin_10007200(self) -> Location:
        return Location(city=self.value, area=Name(name="二林鎮", code="10007200"))

    @property
    def tian_wei_10007210(self) -> Location:
        return Location(city=self.value, area=Name(name="田尾鄉", code="10007210"))

    @property
    def pi_tou_10007220(self) -> Location:
        return Location(city=self.value, area=Name(name="埤頭鄉", code="10007220"))

    @property
    def fang_yuan_10007230(self) -> Location:
        return Location(city=self.value, area=Name(name="芳苑鄉", code="10007230"))

    @property
    def da_cheng_10007240(self) -> Location:
        return Location(city=self.value, area=Name(name="大城鄉", code="10007240"))

    @property
    def zhu_tang_10007250(self) -> Location:
        return Location(city=self.value, area=Name(name="竹塘鄉", code="10007250"))

    @property
    def xi_zhou_10007260(self) -> Location:
        return Location(city=self.value, area=Name(name="溪州鄉", code="10007260"))
