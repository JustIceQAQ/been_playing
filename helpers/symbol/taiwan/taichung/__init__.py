from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TaichungCity(Enum):
    CITY = Name(name="臺中市", code="66000000", ios3166ma=ISO3166Ma.TAICHUNG_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def central_66000010(self) -> Location:
        return Location(city=self.value, area=Name(name="中區", code="66000010"))

    @property
    def east_66000020(self) -> Location:
        return Location(city=self.value, area=Name(name="東區", code="66000020"))

    @property
    def south_66000030(self) -> Location:
        return Location(city=self.value, area=Name(name="南區", code="66000030"))

    @property
    def west_66000040(self) -> Location:
        return Location(city=self.value, area=Name(name="西區", code="66000040"))

    @property
    def north_66000050(self) -> Location:
        return Location(city=self.value, area=Name(name="北區", code="66000050"))

    @property
    def xitun_66000060(self) -> Location:
        return Location(city=self.value, area=Name(name="西屯區", code="66000060"))

    @property
    def nantun_66000070(self) -> Location:
        return Location(city=self.value, area=Name(name="南屯區", code="66000070"))

    @property
    def beitun_66000080(self) -> Location:
        return Location(city=self.value, area=Name(name="北屯區", code="66000080"))

    @property
    def fengyuan_66000090(self) -> Location:
        return Location(city=self.value, area=Name(name="豐原區", code="66000090"))

    @property
    def dongshi_66000100(self) -> Location:
        return Location(city=self.value, area=Name(name="東勢區", code="66000100"))

    @property
    def dajia_66000110(self) -> Location:
        return Location(city=self.value, area=Name(name="大甲區", code="66000110"))

    @property
    def qingshui_66000120(self) -> Location:
        return Location(city=self.value, area=Name(name="清水區", code="66000120"))

    @property
    def shalu_66000130(self) -> Location:
        return Location(city=self.value, area=Name(name="沙鹿區", code="66000130"))

    @property
    def wuqi_66000140(self) -> Location:
        return Location(city=self.value, area=Name(name="梧棲區", code="66000140"))

    @property
    def houli_66000150(self) -> Location:
        return Location(city=self.value, area=Name(name="后里區", code="66000150"))

    @property
    def shengang_66000160(self) -> Location:
        return Location(city=self.value, area=Name(name="神岡區", code="66000160"))

    @property
    def tanzi_66000170(self) -> Location:
        return Location(city=self.value, area=Name(name="潭子區", code="66000170"))

    @property
    def daya_66000180(self) -> Location:
        return Location(city=self.value, area=Name(name="大雅區", code="66000180"))

    @property
    def xinshe_66000190(self) -> Location:
        return Location(city=self.value, area=Name(name="新社區", code="66000190"))

    @property
    def shigang_66000200(self) -> Location:
        return Location(city=self.value, area=Name(name="石岡區", code="66000200"))

    @property
    def waipu_66000210(self) -> Location:
        return Location(city=self.value, area=Name(name="外埔區", code="66000210"))

    @property
    def daan_66000220(self) -> Location:
        return Location(city=self.value, area=Name(name="大安區", code="66000220"))

    @property
    def wuri_66000230(self) -> Location:
        return Location(city=self.value, area=Name(name="烏日區", code="66000230"))

    @property
    def dadu_66000240(self) -> Location:
        return Location(city=self.value, area=Name(name="大肚區", code="66000240"))

    @property
    def longjing_66000250(self) -> Location:
        return Location(city=self.value, area=Name(name="龍井區", code="66000250"))

    @property
    def wufeng_66000260(self) -> Location:
        return Location(city=self.value, area=Name(name="霧峰區", code="66000260"))

    @property
    def taiping_66000270(self) -> Location:
        return Location(city=self.value, area=Name(name="太平區", code="66000270"))

    @property
    def dali_66000280(self) -> Location:
        return Location(city=self.value, area=Name(name="大里區", code="66000280"))

    @property
    def heping_66000290(self) -> Location:
        return Location(city=self.value, area=Name(name="和平區", code="66000290"))
