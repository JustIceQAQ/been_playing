from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TaichungCity(Enum):
    CITY = Name(name="臺中市", code="66000000", ios3166ma=ISO3166Ma.TAICHUNG_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def zhong_66000010(self) -> Location:
        return Location(city=self.value, area=Name(name="中區", code="66000010"))

    @property
    def dong_66000020(self) -> Location:
        return Location(city=self.value, area=Name(name="東區", code="66000020"))

    @property
    def nan_66000030(self) -> Location:
        return Location(city=self.value, area=Name(name="南區", code="66000030"))

    @property
    def xi_66000040(self) -> Location:
        return Location(city=self.value, area=Name(name="西區", code="66000040"))

    @property
    def bei_66000050(self) -> Location:
        return Location(city=self.value, area=Name(name="北區", code="66000050"))

    @property
    def xi_tun_66000060(self) -> Location:
        return Location(city=self.value, area=Name(name="西屯區", code="66000060"))

    @property
    def nan_tun_66000070(self) -> Location:
        return Location(city=self.value, area=Name(name="南屯區", code="66000070"))

    @property
    def bei_tun_66000080(self) -> Location:
        return Location(city=self.value, area=Name(name="北屯區", code="66000080"))

    @property
    def feng_yuan_66000090(self) -> Location:
        return Location(city=self.value, area=Name(name="豐原區", code="66000090"))

    @property
    def dong_shi_66000100(self) -> Location:
        return Location(city=self.value, area=Name(name="東勢區", code="66000100"))

    @property
    def da_jia_66000110(self) -> Location:
        return Location(city=self.value, area=Name(name="大甲區", code="66000110"))

    @property
    def qing_shui_66000120(self) -> Location:
        return Location(city=self.value, area=Name(name="清水區", code="66000120"))

    @property
    def sha_lu_66000130(self) -> Location:
        return Location(city=self.value, area=Name(name="沙鹿區", code="66000130"))

    @property
    def wu_qi_66000140(self) -> Location:
        return Location(city=self.value, area=Name(name="梧棲區", code="66000140"))

    @property
    def hou_li_66000150(self) -> Location:
        return Location(city=self.value, area=Name(name="后里區", code="66000150"))

    @property
    def shen_gang_66000160(self) -> Location:
        return Location(city=self.value, area=Name(name="神岡區", code="66000160"))

    @property
    def tan_zi_66000170(self) -> Location:
        return Location(city=self.value, area=Name(name="潭子區", code="66000170"))

    @property
    def da_ya_66000180(self) -> Location:
        return Location(city=self.value, area=Name(name="大雅區", code="66000180"))

    @property
    def xin_she_66000190(self) -> Location:
        return Location(city=self.value, area=Name(name="新社區", code="66000190"))

    @property
    def shi_gang_66000200(self) -> Location:
        return Location(city=self.value, area=Name(name="石岡區", code="66000200"))

    @property
    def wai_pu_66000210(self) -> Location:
        return Location(city=self.value, area=Name(name="外埔區", code="66000210"))

    @property
    def da_an_66000220(self) -> Location:
        return Location(city=self.value, area=Name(name="大安區", code="66000220"))

    @property
    def wu_ri_66000230(self) -> Location:
        return Location(city=self.value, area=Name(name="烏日區", code="66000230"))

    @property
    def da_du_66000240(self) -> Location:
        return Location(city=self.value, area=Name(name="大肚區", code="66000240"))

    @property
    def long_jing_66000250(self) -> Location:
        return Location(city=self.value, area=Name(name="龍井區", code="66000250"))

    @property
    def wu_feng_66000260(self) -> Location:
        return Location(city=self.value, area=Name(name="霧峰區", code="66000260"))

    @property
    def tai_ping_66000270(self) -> Location:
        return Location(city=self.value, area=Name(name="太平區", code="66000270"))

    @property
    def da_li_66000280(self) -> Location:
        return Location(city=self.value, area=Name(name="大里區", code="66000280"))

    @property
    def he_ping_66000290(self) -> Location:
        return Location(city=self.value, area=Name(name="和平區", code="66000290"))
