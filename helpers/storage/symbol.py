from enum import Enum


class TaiwanCity(str, Enum):
    # 縣 (Counties) - 代碼多源於 ISO 3166/MA
    changhua_county = "TW-CHA"  # 彰化縣 (Changhua County) - 來源: ISO 3166/MA
    chiayi_county = "TW-CYQ"  # 嘉義縣 (Chiayi County) - 來源: ISO 3166/MA
    hsinchu_county = "TW-HSQ"  # 新竹縣 (Hsinchu County) - 來源: ISO 3166/MA
    hualien_county = "TW-HUA"  # 花蓮縣 (Hualien County) - 來源: ISO 3166/MA
    yilan_county = "TW-ILA"  # 宜蘭縣 (Yilan County) - 來源: ISO 3166/MA
    kinmen_county = "TW-KIN"  # 金門縣 (Kinmen County) - 來源: ISO 3166/MA
    lienchiang_county = "TW-LIE"  # 連江縣 (Lienchiang County) - 來源: ISO 3166/MA
    miaoli_county = "TW-MIA"  # 苗栗縣 (Miaoli County) - 來源: ISO 3166/MA
    nantou_county = "TW-NAN"  # 南投縣 (Nantou County) - 來源: ISO 3166/MA
    penghu_county = "TW-PEN"  # 澎湖縣 (Penghu County) - 來源: ISO 3166/MA
    pingtung_county = "TW-PIF"  # 屏東縣 (Pingtung County) - 來源: IATA
    taitung_county = "TW-TTT"  # 臺東縣 (Taitung County) - 來源: IATA
    yunlin_county = "TW-YUN"  # 雲林縣 (Yunlin County) - 來源: ISO 3166/MA

    # 市 (Cities) / 直轄市 (Special Municipalities) - 代碼多源於 IATA
    chiayi_city = "TW-CYI"  # 嘉義市 (Chiayi City) - 來源: IATA
    hsinchu_city = "TW-HSZ"  # 新竹市 (Hsinchu City) - 來源: IATA
    keelung_city = "TW-KEE"  # 基隆市 (Keelung City) - 來源: ISO 3166/MA
    kaohsiung_city = "TW-KHH"  # 高雄市 (Kaohsiung City) - 來源: IATA
    new_taipei_city = "TW-NWT"  # 新北市 (New Taipei City) - 來源: ISO 3166/MA
    taoyuan_city = "TW-TAO"  # 桃園市 (Taoyuan City) - 來源: ISO 3166/MA
    tainan_city = "TW-TNN"  # 臺南市 (Tainan City) - 來源: IATA
    taipei_city = "TW-TPE"  # 臺北市 (Taipei City) - 來源: IATA
    taichung_city = "TW-TXG"  # 臺中市 (Taichung City) - 來源: IATA
