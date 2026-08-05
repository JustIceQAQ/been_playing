from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TaoyuanCity(Enum):
    CITY = Name(name="桃園市", code="68000000", ios3166ma=ISO3166Ma.TAOYUAN_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def taoyuan_68000010(self) -> Location:
        return Location(city=self.value, area=Name(name="桃園區", code="68000010"))

    @property
    def zhongli_68000020(self) -> Location:
        return Location(city=self.value, area=Name(name="中壢區", code="68000020"))

    @property
    def daxi_68000030(self) -> Location:
        return Location(city=self.value, area=Name(name="大溪區", code="68000030"))

    @property
    def yangmei_68000040(self) -> Location:
        return Location(city=self.value, area=Name(name="楊梅區", code="68000040"))

    @property
    def luzhu_68000050(self) -> Location:
        return Location(city=self.value, area=Name(name="蘆竹區", code="68000050"))

    @property
    def dayuan_68000060(self) -> Location:
        return Location(city=self.value, area=Name(name="大園區", code="68000060"))

    @property
    def guishan_68000070(self) -> Location:
        return Location(city=self.value, area=Name(name="龜山區", code="68000070"))

    @property
    def bade_68000080(self) -> Location:
        return Location(city=self.value, area=Name(name="八德區", code="68000080"))

    @property
    def longtan_68000090(self) -> Location:
        return Location(city=self.value, area=Name(name="龍潭區", code="68000090"))

    @property
    def pingzhen_68000100(self) -> Location:
        return Location(city=self.value, area=Name(name="平鎮區", code="68000100"))

    @property
    def xinwu_68000110(self) -> Location:
        return Location(city=self.value, area=Name(name="新屋區", code="68000110"))

    @property
    def guanyin_68000120(self) -> Location:
        return Location(city=self.value, area=Name(name="觀音區", code="68000120"))

    @property
    def fuxing_68000130(self) -> Location:
        return Location(city=self.value, area=Name(name="復興區", code="68000130"))
