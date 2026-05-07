from helpers.symbol.taiwan.taipei import TaipeiCity
from helpers.symbol.taiwan.kaohsiung import KaohsiungCity
from helpers.symbol.taiwan.new_taipei import NewTaipeiCity
from helpers.symbol.taiwan.taichung import TaichungCity
from helpers.symbol.taiwan.tainan import TainanCity
from helpers.symbol.taiwan.taoyuan import TaoyuanCity
from helpers.symbol.taiwan.keelung import KeelungCity
from helpers.symbol.taiwan.hsinchu_city import HsinchuCity
from helpers.symbol.taiwan.chiayi_city import ChaiyiCity
from helpers.symbol.taiwan.yilan import YilanCounty
from helpers.symbol.taiwan.hsinchu_county import HsinchuCounty
from helpers.symbol.taiwan.miaoli import MiaoliCounty
from helpers.symbol.taiwan.changhua import ChanghuaCounty
from helpers.symbol.taiwan.nantou import NantouCounty
from helpers.symbol.taiwan.yunlin import YunlinCounty
from helpers.symbol.taiwan.chiayi_county import ChaiyiCounty
from helpers.symbol.taiwan.pingtung import PingtungCounty
from helpers.symbol.taiwan.taitung import TaitungCounty
from helpers.symbol.taiwan.hualien import HualienCounty
from helpers.symbol.taiwan.penghu import PenghuCounty
from helpers.symbol.taiwan.lienchiang import LienchiangCounty
from helpers.symbol.taiwan.kinmen import KinmenCounty

__all__ = [
    "Taiwan",
]


class Taiwan:
    taipei: TaipeiCity = TaipeiCity.CITY  # 臺北市
    kaohsiung: KaohsiungCity = KaohsiungCity.CITY  # 高雄市
    new_taipei: NewTaipeiCity = NewTaipeiCity.CITY  # 新北市
    taichung: TaichungCity = TaichungCity.CITY  # 臺中市
    tainan: TainanCity = TainanCity.CITY  # 臺南市
    taoyuan: TaoyuanCity = TaoyuanCity.CITY  # 桃園市
    keelung: KeelungCity = KeelungCity.CITY  # 基隆市
    hsinchu_city: HsinchuCity = HsinchuCity.CITY  # 新竹市
    chiayi_city: ChaiyiCity = ChaiyiCity.CITY  # 嘉義市
    yilan: YilanCounty = YilanCounty.CITY  # 宜蘭縣
    hsinchu_county: HsinchuCounty = HsinchuCounty.CITY  # 新竹縣
    miaoli: MiaoliCounty = MiaoliCounty.CITY  # 苗栗縣
    changhua: ChanghuaCounty = ChanghuaCounty.CITY  # 彰化縣
    nantou: NantouCounty = NantouCounty.CITY  # 南投縣
    yunlin: YunlinCounty = YunlinCounty.CITY  # 雲林縣
    chiayi_county: ChaiyiCounty = ChaiyiCounty.CITY  # 嘉義縣
    pingtung: PingtungCounty = PingtungCounty.CITY  # 屏東縣
    taitung: TaitungCounty = TaitungCounty.CITY  # 臺東縣
    hualien: HualienCounty = HualienCounty.CITY  # 花蓮縣
    penghu: PenghuCounty = PenghuCounty.CITY  # 澎湖縣
    lienchiang: LienchiangCounty = LienchiangCounty.CITY  # 連江縣
    kinmen: KinmenCounty = KinmenCounty.CITY  # 金門縣
