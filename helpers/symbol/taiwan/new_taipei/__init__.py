from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class NewTaipeiCity(Enum):
    CITY = Name(name="新北市", code="65000000", ios3166ma=ISO3166Ma.NEW_TAIPEI_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def ban_qiao_65000010(self) -> Location:
        return Location(city=self.value, area=Name(name="板橋區", code="65000010"))

    @property
    def san_chong_65000020(self) -> Location:
        return Location(city=self.value, area=Name(name="三重區", code="65000020"))

    @property
    def zhong_he_65000030(self) -> Location:
        return Location(city=self.value, area=Name(name="中和區", code="65000030"))

    @property
    def yong_he_65000040(self) -> Location:
        return Location(city=self.value, area=Name(name="永和區", code="65000040"))

    @property
    def xin_zhuang_65000050(self) -> Location:
        return Location(city=self.value, area=Name(name="新莊區", code="65000050"))

    @property
    def xin_dian_65000060(self) -> Location:
        return Location(city=self.value, area=Name(name="新店區", code="65000060"))

    @property
    def shu_lin_65000070(self) -> Location:
        return Location(city=self.value, area=Name(name="樹林區", code="65000070"))

    @property
    def ying_ge_65000080(self) -> Location:
        return Location(city=self.value, area=Name(name="鶯歌區", code="65000080"))

    @property
    def san_xia_65000090(self) -> Location:
        return Location(city=self.value, area=Name(name="三峽區", code="65000090"))

    @property
    def dan_shui_65000100(self) -> Location:
        return Location(city=self.value, area=Name(name="淡水區", code="65000100"))

    @property
    def xi_zhi_65000110(self) -> Location:
        return Location(city=self.value, area=Name(name="汐止區", code="65000110"))

    @property
    def rui_fang_65000120(self) -> Location:
        return Location(city=self.value, area=Name(name="瑞芳區", code="65000120"))

    @property
    def tu_cheng_65000130(self) -> Location:
        return Location(city=self.value, area=Name(name="土城區", code="65000130"))

    @property
    def lu_zhou_65000140(self) -> Location:
        return Location(city=self.value, area=Name(name="蘆洲區", code="65000140"))

    @property
    def wu_gu_65000150(self) -> Location:
        return Location(city=self.value, area=Name(name="五股區", code="65000150"))

    @property
    def tai_shan_65000160(self) -> Location:
        return Location(city=self.value, area=Name(name="泰山區", code="65000160"))

    @property
    def lin_kou_65000170(self) -> Location:
        return Location(city=self.value, area=Name(name="林口區", code="65000170"))

    @property
    def shen_keng_65000180(self) -> Location:
        return Location(city=self.value, area=Name(name="深坑區", code="65000180"))

    @property
    def shi_ding_65000190(self) -> Location:
        return Location(city=self.value, area=Name(name="石碇區", code="65000190"))

    @property
    def ping_lin_65000200(self) -> Location:
        return Location(city=self.value, area=Name(name="坪林區", code="65000200"))

    @property
    def san_zhi_65000210(self) -> Location:
        return Location(city=self.value, area=Name(name="三芝區", code="65000210"))

    @property
    def shi_men_65000220(self) -> Location:
        return Location(city=self.value, area=Name(name="石門區", code="65000220"))

    @property
    def ba_li_65000230(self) -> Location:
        return Location(city=self.value, area=Name(name="八里區", code="65000230"))

    @property
    def ping_xi_65000240(self) -> Location:
        return Location(city=self.value, area=Name(name="平溪區", code="65000240"))

    @property
    def shuang_xi_65000250(self) -> Location:
        return Location(city=self.value, area=Name(name="雙溪區", code="65000250"))

    @property
    def gong_liao_65000260(self) -> Location:
        return Location(city=self.value, area=Name(name="貢寮區", code="65000260"))

    @property
    def jin_shan_65000270(self) -> Location:
        return Location(city=self.value, area=Name(name="金山區", code="65000270"))

    @property
    def wan_li_65000280(self) -> Location:
        return Location(city=self.value, area=Name(name="萬里區", code="65000280"))

    @property
    def wu_lai_65000290(self) -> Location:
        return Location(city=self.value, area=Name(name="烏來區", code="65000290"))
