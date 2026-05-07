from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TaoyuanCity(Enum):
    CITY = Name(name="桃園市", code="68000000", ios3166ma=ISO3166Ma.TAOYUAN_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def tao_yuan_68000010(self) -> Location:
        return Location(city=self.value, area=Name(name="桃園區", code="68000010"))

    @property
    def zhong_li_68000020(self) -> Location:
        return Location(city=self.value, area=Name(name="中壢區", code="68000020"))

    @property
    def da_xi_68000030(self) -> Location:
        return Location(city=self.value, area=Name(name="大溪區", code="68000030"))

    @property
    def yang_mei_68000040(self) -> Location:
        return Location(city=self.value, area=Name(name="楊梅區", code="68000040"))

    @property
    def lu_zhu_68000050(self) -> Location:
        return Location(city=self.value, area=Name(name="蘆竹區", code="68000050"))

    @property
    def da_yuan_68000060(self) -> Location:
        return Location(city=self.value, area=Name(name="大園區", code="68000060"))

    @property
    def gui_shan_68000070(self) -> Location:
        return Location(city=self.value, area=Name(name="龜山區", code="68000070"))

    @property
    def ba_de_68000080(self) -> Location:
        return Location(city=self.value, area=Name(name="八德區", code="68000080"))

    @property
    def long_tan_68000090(self) -> Location:
        return Location(city=self.value, area=Name(name="龍潭區", code="68000090"))

    @property
    def ping_zhen_68000100(self) -> Location:
        return Location(city=self.value, area=Name(name="平鎮區", code="68000100"))

    @property
    def xin_wu_68000110(self) -> Location:
        return Location(city=self.value, area=Name(name="新屋區", code="68000110"))

    @property
    def guan_yin_68000120(self) -> Location:
        return Location(city=self.value, area=Name(name="觀音區", code="68000120"))

    @property
    def fu_xing_68000130(self) -> Location:
        return Location(city=self.value, area=Name(name="復興區", code="68000130"))
