from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class NantouCounty(Enum):
    CITY = Name(name="南投縣", code="10008000", ios3166ma=ISO3166Ma.NANTOU_COUNTY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def nan_tou_10008010(self) -> Location:
        return Location(city=self.value, area=Name(name="南投市", code="10008010"))

    @property
    def pu_li_10008020(self) -> Location:
        return Location(city=self.value, area=Name(name="埔里鎮", code="10008020"))

    @property
    def cao_tun_10008030(self) -> Location:
        return Location(city=self.value, area=Name(name="草屯鎮", code="10008030"))

    @property
    def zhu_shan_10008040(self) -> Location:
        return Location(city=self.value, area=Name(name="竹山鎮", code="10008040"))

    @property
    def ji_ji_10008050(self) -> Location:
        return Location(city=self.value, area=Name(name="集集鎮", code="10008050"))

    @property
    def ming_jian_10008060(self) -> Location:
        return Location(city=self.value, area=Name(name="名間鄉", code="10008060"))

    @property
    def lu_gu_10008070(self) -> Location:
        return Location(city=self.value, area=Name(name="鹿谷鄉", code="10008070"))

    @property
    def zhong_liao_10008080(self) -> Location:
        return Location(city=self.value, area=Name(name="中寮鄉", code="10008080"))

    @property
    def yu_chi_10008090(self) -> Location:
        return Location(city=self.value, area=Name(name="魚池鄉", code="10008090"))

    @property
    def guo_xing_10008100(self) -> Location:
        return Location(city=self.value, area=Name(name="國姓鄉", code="10008100"))

    @property
    def shui_li_10008110(self) -> Location:
        return Location(city=self.value, area=Name(name="水里鄉", code="10008110"))

    @property
    def xin_yi_10008120(self) -> Location:
        return Location(city=self.value, area=Name(name="信義鄉", code="10008120"))

    @property
    def ren_ai_10008130(self) -> Location:
        return Location(city=self.value, area=Name(name="仁愛鄉", code="10008130"))
