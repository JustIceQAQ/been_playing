from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class TainanCity(Enum):
    CITY = Name(name="臺南市", code="67000000", ios3166ma=ISO3166Ma.TAINAN_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def xin_ying_67000010(self) -> Location:
        return Location(city=self.value, area=Name(name="新營區", code="67000010"))

    @property
    def yan_shui_67000020(self) -> Location:
        return Location(city=self.value, area=Name(name="鹽水區", code="67000020"))

    @property
    def bai_he_67000030(self) -> Location:
        return Location(city=self.value, area=Name(name="白河區", code="67000030"))

    @property
    def liu_ying_67000040(self) -> Location:
        return Location(city=self.value, area=Name(name="柳營區", code="67000040"))

    @property
    def hou_bi_67000050(self) -> Location:
        return Location(city=self.value, area=Name(name="後壁區", code="67000050"))

    @property
    def dong_shan_67000060(self) -> Location:
        return Location(city=self.value, area=Name(name="東山區", code="67000060"))

    @property
    def ma_dou_67000070(self) -> Location:
        return Location(city=self.value, area=Name(name="麻豆區", code="67000070"))

    @property
    def xia_ying_67000080(self) -> Location:
        return Location(city=self.value, area=Name(name="下營區", code="67000080"))

    @property
    def liu_jia_67000090(self) -> Location:
        return Location(city=self.value, area=Name(name="六甲區", code="67000090"))

    @property
    def guan_tian_67000100(self) -> Location:
        return Location(city=self.value, area=Name(name="官田區", code="67000100"))

    @property
    def da_nei_67000110(self) -> Location:
        return Location(city=self.value, area=Name(name="大內區", code="67000110"))

    @property
    def jia_li_67000120(self) -> Location:
        return Location(city=self.value, area=Name(name="佳里區", code="67000120"))

    @property
    def xue_jia_67000130(self) -> Location:
        return Location(city=self.value, area=Name(name="學甲區", code="67000130"))

    @property
    def xi_gang_67000140(self) -> Location:
        return Location(city=self.value, area=Name(name="西港區", code="67000140"))

    @property
    def qi_gu_67000150(self) -> Location:
        return Location(city=self.value, area=Name(name="七股區", code="67000150"))

    @property
    def jiang_jun_67000160(self) -> Location:
        return Location(city=self.value, area=Name(name="將軍區", code="67000160"))

    @property
    def bei_men_67000170(self) -> Location:
        return Location(city=self.value, area=Name(name="北門區", code="67000170"))

    @property
    def xin_hua_67000180(self) -> Location:
        return Location(city=self.value, area=Name(name="新化區", code="67000180"))

    @property
    def shan_hua_67000190(self) -> Location:
        return Location(city=self.value, area=Name(name="善化區", code="67000190"))

    @property
    def xin_shi_67000200(self) -> Location:
        return Location(city=self.value, area=Name(name="新市區", code="67000200"))

    @property
    def an_ding_67000210(self) -> Location:
        return Location(city=self.value, area=Name(name="安定區", code="67000210"))

    @property
    def shan_shang_67000220(self) -> Location:
        return Location(city=self.value, area=Name(name="山上區", code="67000220"))

    @property
    def yu_jing_67000230(self) -> Location:
        return Location(city=self.value, area=Name(name="玉井區", code="67000230"))

    @property
    def nan_xi_67000240(self) -> Location:
        return Location(city=self.value, area=Name(name="楠西區", code="67000240"))

    @property
    def nan_hua_67000250(self) -> Location:
        return Location(city=self.value, area=Name(name="南化區", code="67000250"))

    @property
    def zuo_zhen_67000260(self) -> Location:
        return Location(city=self.value, area=Name(name="左鎮區", code="67000260"))

    @property
    def ren_de_67000270(self) -> Location:
        return Location(city=self.value, area=Name(name="仁德區", code="67000270"))

    @property
    def gui_ren_67000280(self) -> Location:
        return Location(city=self.value, area=Name(name="歸仁區", code="67000280"))

    @property
    def guan_miao_67000290(self) -> Location:
        return Location(city=self.value, area=Name(name="關廟區", code="67000290"))

    @property
    def long_qi_67000300(self) -> Location:
        return Location(city=self.value, area=Name(name="龍崎區", code="67000300"))

    @property
    def yong_kang_67000310(self) -> Location:
        return Location(city=self.value, area=Name(name="永康區", code="67000310"))

    @property
    def dong_67000320(self) -> Location:
        return Location(city=self.value, area=Name(name="東區", code="67000320"))

    @property
    def nan_67000330(self) -> Location:
        return Location(city=self.value, area=Name(name="南區", code="67000330"))

    @property
    def bei_67000340(self) -> Location:
        return Location(city=self.value, area=Name(name="北區", code="67000340"))

    @property
    def an_nan_67000350(self) -> Location:
        return Location(city=self.value, area=Name(name="安南區", code="67000350"))

    @property
    def an_ping_67000360(self) -> Location:
        return Location(city=self.value, area=Name(name="安平區", code="67000360"))

    @property
    def zhong_xi_67000370(self) -> Location:
        return Location(city=self.value, area=Name(name="中西區", code="67000370"))
