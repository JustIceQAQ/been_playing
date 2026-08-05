from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TainanCity(Enum):
    CITY = Name(name="臺南市", code="67000000", ios3166ma=ISO3166Ma.TAINAN_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def xinying_67000010(self) -> Location:
        return Location(city=self.value, area=Name(name="新營區", code="67000010"))

    @property
    def yanshui_67000020(self) -> Location:
        return Location(city=self.value, area=Name(name="鹽水區", code="67000020"))

    @property
    def baihe_67000030(self) -> Location:
        return Location(city=self.value, area=Name(name="白河區", code="67000030"))

    @property
    def liuying_67000040(self) -> Location:
        return Location(city=self.value, area=Name(name="柳營區", code="67000040"))

    @property
    def houbi_67000050(self) -> Location:
        return Location(city=self.value, area=Name(name="後壁區", code="67000050"))

    @property
    def dongshan_67000060(self) -> Location:
        return Location(city=self.value, area=Name(name="東山區", code="67000060"))

    @property
    def madou_67000070(self) -> Location:
        return Location(city=self.value, area=Name(name="麻豆區", code="67000070"))

    @property
    def xiaying_67000080(self) -> Location:
        return Location(city=self.value, area=Name(name="下營區", code="67000080"))

    @property
    def liujia_67000090(self) -> Location:
        return Location(city=self.value, area=Name(name="六甲區", code="67000090"))

    @property
    def guantian_67000100(self) -> Location:
        return Location(city=self.value, area=Name(name="官田區", code="67000100"))

    @property
    def danei_67000110(self) -> Location:
        return Location(city=self.value, area=Name(name="大內區", code="67000110"))

    @property
    def jiali_67000120(self) -> Location:
        return Location(city=self.value, area=Name(name="佳里區", code="67000120"))

    @property
    def xuejia_67000130(self) -> Location:
        return Location(city=self.value, area=Name(name="學甲區", code="67000130"))

    @property
    def xigang_67000140(self) -> Location:
        return Location(city=self.value, area=Name(name="西港區", code="67000140"))

    @property
    def qigu_67000150(self) -> Location:
        return Location(city=self.value, area=Name(name="七股區", code="67000150"))

    @property
    def jiangjun_67000160(self) -> Location:
        return Location(city=self.value, area=Name(name="將軍區", code="67000160"))

    @property
    def beimen_67000170(self) -> Location:
        return Location(city=self.value, area=Name(name="北門區", code="67000170"))

    @property
    def xinhua_67000180(self) -> Location:
        return Location(city=self.value, area=Name(name="新化區", code="67000180"))

    @property
    def shanhua_67000190(self) -> Location:
        return Location(city=self.value, area=Name(name="善化區", code="67000190"))

    @property
    def xinshi_67000200(self) -> Location:
        return Location(city=self.value, area=Name(name="新市區", code="67000200"))

    @property
    def anding_67000210(self) -> Location:
        return Location(city=self.value, area=Name(name="安定區", code="67000210"))

    @property
    def shanshang_67000220(self) -> Location:
        return Location(city=self.value, area=Name(name="山上區", code="67000220"))

    @property
    def yujing_67000230(self) -> Location:
        return Location(city=self.value, area=Name(name="玉井區", code="67000230"))

    @property
    def nanxi_67000240(self) -> Location:
        return Location(city=self.value, area=Name(name="楠西區", code="67000240"))

    @property
    def nanhua_67000250(self) -> Location:
        return Location(city=self.value, area=Name(name="南化區", code="67000250"))

    @property
    def zuozhen_67000260(self) -> Location:
        return Location(city=self.value, area=Name(name="左鎮區", code="67000260"))

    @property
    def rende_67000270(self) -> Location:
        return Location(city=self.value, area=Name(name="仁德區", code="67000270"))

    @property
    def guiren_67000280(self) -> Location:
        return Location(city=self.value, area=Name(name="歸仁區", code="67000280"))

    @property
    def guanmiao_67000290(self) -> Location:
        return Location(city=self.value, area=Name(name="關廟區", code="67000290"))

    @property
    def longqi_67000300(self) -> Location:
        return Location(city=self.value, area=Name(name="龍崎區", code="67000300"))

    @property
    def yongkang_67000310(self) -> Location:
        return Location(city=self.value, area=Name(name="永康區", code="67000310"))

    @property
    def east_67000320(self) -> Location:
        return Location(city=self.value, area=Name(name="東區", code="67000320"))

    @property
    def south_67000330(self) -> Location:
        return Location(city=self.value, area=Name(name="南區", code="67000330"))

    @property
    def north_67000340(self) -> Location:
        return Location(city=self.value, area=Name(name="北區", code="67000340"))

    @property
    def annan_67000350(self) -> Location:
        return Location(city=self.value, area=Name(name="安南區", code="67000350"))

    @property
    def anping_67000360(self) -> Location:
        return Location(city=self.value, area=Name(name="安平區", code="67000360"))

    @property
    def west_central_67000370(self) -> Location:
        return Location(city=self.value, area=Name(name="中西區", code="67000370"))
