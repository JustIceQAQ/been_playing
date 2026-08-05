from enum import StrEnum


class ISO3166Ma(StrEnum):
    # 縣 (Counties) - 代碼多源於 ISO 3166/MA
    CHANGHUA_COUNTY = "TW-CHA"  # 彰化縣 (Changhua County) - 來源: ISO 3166/MA
    CHIAYI_COUNTY = "TW-CYQ"  # 嘉義縣 (Chiayi County) - 來源: ISO 3166/MA
    HSINCHU_COUNTY = "TW-HSQ"  # 新竹縣 (Hsinchu County) - 來源: ISO 3166/MA
    HUALIEN_COUNTY = "TW-HUA"  # 花蓮縣 (Hualien County) - 來源: ISO 3166/MA
    YILAN_COUNTY = "TW-ILA"  # 宜蘭縣 (Yilan County) - 來源: ISO 3166/MA
    KINMEN_COUNTY = "TW-KIN"  # 金門縣 (Kinmen County) - 來源: ISO 3166/MA
    LIENCHIANG_COUNTY = "TW-LIE"  # 連江縣 (Lienchiang County) - 來源: ISO 3166/MA
    MIAOLI_COUNTY = "TW-MIA"  # 苗栗縣 (Miaoli County) - 來源: ISO 3166/MA
    NANTOU_COUNTY = "TW-NAN"  # 南投縣 (Nantou County) - 來源: ISO 3166/MA
    PENGHU_COUNTY = "TW-PEN"  # 澎湖縣 (Penghu County) - 來源: ISO 3166/MA
    PINGTUNG_COUNTY = "TW-PIF"  # 屏東縣 (Pingtung County) - 來源: IATA
    TAITUNG_COUNTY = "TW-TTT"  # 臺東縣 (Taitung County) - 來源: IATA
    YUNLIN_COUNTY = "TW-YUN"  # 雲林縣 (Yunlin County) - 來源: ISO 3166/MA

    # 市 (Cities) / 直轄市 (Special Municipalities) - 代碼多源於 IATA
    CHIAYI_CITY = "TW-CYI"  # 嘉義市 (Chiayi City) - 來源: IATA
    HSINCHU_CITY = "TW-HSZ"  # 新竹市 (Hsinchu City) - 來源: IATA
    KEELUNG_CITY = "TW-KEE"  # 基隆市 (Keelung City) - 來源: ISO 3166/MA
    KAOHSIUNG_CITY = "TW-KHH"  # 高雄市 (Kaohsiung City) - 來源: IATA
    NEW_TAIPEI_CITY = "TW-NWT"  # 新北市 (New Taipei City) - 來源: ISO 3166/MA
    TAOYUAN_CITY = "TW-TAO"  # 桃園市 (Taoyuan City) - 來源: ISO 3166/MA
    TAINAN_CITY = "TW-TNN"  # 臺南市 (Tainan City) - 來源: IATA
    TAIPEI_CITY = "TW-TPE"  # 臺北市 (Taipei City) - 來源: IATA
    TAICHUNG_CITY = "TW-TXG"  # 臺中市 (Taichung City) - 來源: IATA
