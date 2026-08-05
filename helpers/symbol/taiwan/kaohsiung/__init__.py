from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class KaohsiungCity(Enum):
    CITY = Name(name="高雄市", code="64000000", ios3166ma=ISO3166Ma.KAOHSIUNG_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def yancheng_64000010(self) -> Location:
        return Location(city=self.value, area=Name(name="鹽埕區", code="64000010"))

    @property
    def gushan_64000020(self) -> Location:
        return Location(city=self.value, area=Name(name="鼓山區", code="64000020"))

    @property
    def zuoying_64000030(self) -> Location:
        return Location(city=self.value, area=Name(name="左營區", code="64000030"))

    @property
    def nanzi_64000040(self) -> Location:
        return Location(city=self.value, area=Name(name="楠梓區", code="64000040"))

    @property
    def sanmin_64000050(self) -> Location:
        return Location(city=self.value, area=Name(name="三民區", code="64000050"))

    @property
    def xinxing_64000060(self) -> Location:
        return Location(city=self.value, area=Name(name="新興區", code="64000060"))

    @property
    def qianjin_64000070(self) -> Location:
        return Location(city=self.value, area=Name(name="前金區", code="64000070"))

    @property
    def lingya_64000080(self) -> Location:
        return Location(city=self.value, area=Name(name="苓雅區", code="64000080"))

    @property
    def qianzhen_64000090(self) -> Location:
        return Location(city=self.value, area=Name(name="前鎮區", code="64000090"))

    @property
    def qijin_64000100(self) -> Location:
        return Location(city=self.value, area=Name(name="旗津區", code="64000100"))

    @property
    def xiaogang_64000110(self) -> Location:
        return Location(city=self.value, area=Name(name="小港區", code="64000110"))

    @property
    def fengshan_64000120(self) -> Location:
        return Location(city=self.value, area=Name(name="鳳山區", code="64000120"))

    @property
    def linyuan_64000130(self) -> Location:
        return Location(city=self.value, area=Name(name="林園區", code="64000130"))

    @property
    def daliao_64000140(self) -> Location:
        return Location(city=self.value, area=Name(name="大寮區", code="64000140"))

    @property
    def dashu_64000150(self) -> Location:
        return Location(city=self.value, area=Name(name="大樹區", code="64000150"))

    @property
    def dashe_64000160(self) -> Location:
        return Location(city=self.value, area=Name(name="大社區", code="64000160"))

    @property
    def renwu_64000170(self) -> Location:
        return Location(city=self.value, area=Name(name="仁武區", code="64000170"))

    @property
    def niaosong_64000180(self) -> Location:
        return Location(city=self.value, area=Name(name="鳥松區", code="64000180"))

    @property
    def gangshan_64000190(self) -> Location:
        return Location(city=self.value, area=Name(name="岡山區", code="64000190"))

    @property
    def qiaotou_64000200(self) -> Location:
        return Location(city=self.value, area=Name(name="橋頭區", code="64000200"))

    @property
    def yanchao_64000210(self) -> Location:
        return Location(city=self.value, area=Name(name="燕巢區", code="64000210"))

    @property
    def tianliao_64000220(self) -> Location:
        return Location(city=self.value, area=Name(name="田寮區", code="64000220"))

    @property
    def alian_64000230(self) -> Location:
        return Location(city=self.value, area=Name(name="阿蓮區", code="64000230"))

    @property
    def luzhu_64000240(self) -> Location:
        return Location(city=self.value, area=Name(name="路竹區", code="64000240"))

    @property
    def hunei_64000250(self) -> Location:
        return Location(city=self.value, area=Name(name="湖內區", code="64000250"))

    @property
    def qieding_64000260(self) -> Location:
        return Location(city=self.value, area=Name(name="茄萣區", code="64000260"))

    @property
    def yongan_64000270(self) -> Location:
        return Location(city=self.value, area=Name(name="永安區", code="64000270"))

    @property
    def mituo_64000280(self) -> Location:
        return Location(city=self.value, area=Name(name="彌陀區", code="64000280"))

    @property
    def ziguan_64000290(self) -> Location:
        return Location(city=self.value, area=Name(name="梓官區", code="64000290"))

    @property
    def qishan_64000300(self) -> Location:
        return Location(city=self.value, area=Name(name="旗山區", code="64000300"))

    @property
    def meinong_64000310(self) -> Location:
        return Location(city=self.value, area=Name(name="美濃區", code="64000310"))

    @property
    def liugui_64000320(self) -> Location:
        return Location(city=self.value, area=Name(name="六龜區", code="64000320"))

    @property
    def jiaxian_64000330(self) -> Location:
        return Location(city=self.value, area=Name(name="甲仙區", code="64000330"))

    @property
    def shanlin_64000340(self) -> Location:
        return Location(city=self.value, area=Name(name="杉林區", code="64000340"))

    @property
    def neimen_64000350(self) -> Location:
        return Location(city=self.value, area=Name(name="內門區", code="64000350"))

    @property
    def maolin_64000360(self) -> Location:
        return Location(city=self.value, area=Name(name="茂林區", code="64000360"))

    @property
    def taoyuan_64000370(self) -> Location:
        return Location(city=self.value, area=Name(name="桃源區", code="64000370"))

    @property
    def namaxia_64000380(self) -> Location:
        return Location(city=self.value, area=Name(name="那瑪夏區", code="64000380"))
