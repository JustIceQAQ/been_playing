from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class KaohsiungCity(Enum):
    CITY = Name(name="高雄市", code="64000000", ios3166ma=ISO3166Ma.KAOHSIUNG_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def yan_cheng_64000010(self) -> Location:
        return Location(city=self.value, area=Name(name="鹽埕區", code="64000010"))

    @property
    def gu_shan_64000020(self) -> Location:
        return Location(city=self.value, area=Name(name="鼓山區", code="64000020"))

    @property
    def zuo_ying_64000030(self) -> Location:
        return Location(city=self.value, area=Name(name="左營區", code="64000030"))

    @property
    def nan_zi_64000040(self) -> Location:
        return Location(city=self.value, area=Name(name="楠梓區", code="64000040"))

    @property
    def san_min_64000050(self) -> Location:
        return Location(city=self.value, area=Name(name="三民區", code="64000050"))

    @property
    def xin_xing_64000060(self) -> Location:
        return Location(city=self.value, area=Name(name="新興區", code="64000060"))

    @property
    def qian_jin_64000070(self) -> Location:
        return Location(city=self.value, area=Name(name="前金區", code="64000070"))

    @property
    def ling_ya_64000080(self) -> Location:
        return Location(city=self.value, area=Name(name="苓雅區", code="64000080"))

    @property
    def qian_zhen_64000090(self) -> Location:
        return Location(city=self.value, area=Name(name="前鎮區", code="64000090"))

    @property
    def qi_jin_64000100(self) -> Location:
        return Location(city=self.value, area=Name(name="旗津區", code="64000100"))

    @property
    def xiao_gang_64000110(self) -> Location:
        return Location(city=self.value, area=Name(name="小港區", code="64000110"))

    @property
    def feng_shan_64000120(self) -> Location:
        return Location(city=self.value, area=Name(name="鳳山區", code="64000120"))

    @property
    def lin_yuan_64000130(self) -> Location:
        return Location(city=self.value, area=Name(name="林園區", code="64000130"))

    @property
    def da_liao_64000140(self) -> Location:
        return Location(city=self.value, area=Name(name="大寮區", code="64000140"))

    @property
    def da_shu_64000150(self) -> Location:
        return Location(city=self.value, area=Name(name="大樹區", code="64000150"))

    @property
    def da_she_64000160(self) -> Location:
        return Location(city=self.value, area=Name(name="大社區", code="64000160"))

    @property
    def ren_wu_64000170(self) -> Location:
        return Location(city=self.value, area=Name(name="仁武區", code="64000170"))

    @property
    def niao_song_64000180(self) -> Location:
        return Location(city=self.value, area=Name(name="鳥松區", code="64000180"))

    @property
    def gang_shan_64000190(self) -> Location:
        return Location(city=self.value, area=Name(name="岡山區", code="64000190"))

    @property
    def qiao_tou_64000200(self) -> Location:
        return Location(city=self.value, area=Name(name="橋頭區", code="64000200"))

    @property
    def yan_chao_64000210(self) -> Location:
        return Location(city=self.value, area=Name(name="燕巢區", code="64000210"))

    @property
    def tian_liao_64000220(self) -> Location:
        return Location(city=self.value, area=Name(name="田寮區", code="64000220"))

    @property
    def a_lian_64000230(self) -> Location:
        return Location(city=self.value, area=Name(name="阿蓮區", code="64000230"))

    @property
    def lu_zhu_64000240(self) -> Location:
        return Location(city=self.value, area=Name(name="路竹區", code="64000240"))

    @property
    def hu_nei_64000250(self) -> Location:
        return Location(city=self.value, area=Name(name="湖內區", code="64000250"))

    @property
    def qie_ding_64000260(self) -> Location:
        return Location(city=self.value, area=Name(name="茄萣區", code="64000260"))

    @property
    def yong_an_64000270(self) -> Location:
        return Location(city=self.value, area=Name(name="永安區", code="64000270"))

    @property
    def mi_tuo_64000280(self) -> Location:
        return Location(city=self.value, area=Name(name="彌陀區", code="64000280"))

    @property
    def zi_guan_64000290(self) -> Location:
        return Location(city=self.value, area=Name(name="梓官區", code="64000290"))

    @property
    def qi_shan_64000300(self) -> Location:
        return Location(city=self.value, area=Name(name="旗山區", code="64000300"))

    @property
    def mei_nong_64000310(self) -> Location:
        return Location(city=self.value, area=Name(name="美濃區", code="64000310"))

    @property
    def liu_gui_64000320(self) -> Location:
        return Location(city=self.value, area=Name(name="六龜區", code="64000320"))

    @property
    def jia_xian_64000330(self) -> Location:
        return Location(city=self.value, area=Name(name="甲仙區", code="64000330"))

    @property
    def shan_lin_64000340(self) -> Location:
        return Location(city=self.value, area=Name(name="杉林區", code="64000340"))

    @property
    def nei_men_64000350(self) -> Location:
        return Location(city=self.value, area=Name(name="內門區", code="64000350"))

    @property
    def mao_lin_64000360(self) -> Location:
        return Location(city=self.value, area=Name(name="茂林區", code="64000360"))

    @property
    def tao_yuan_64000370(self) -> Location:
        return Location(city=self.value, area=Name(name="桃源區", code="64000370"))

    @property
    def na_ma_xia_64000380(self) -> Location:
        return Location(city=self.value, area=Name(name="那瑪夏區", code="64000380"))
