from enum import StrEnum, auto


class VenueType(StrEnum):
    # 1. 博物館與歷史類 (重視典藏與研究)
    MUSEUM = auto()  # 綜合性/專題博物館
    MEMORIAL = auto()  # 紀念館/歷史場域

    # 2. 藝術類 (重視展覽與視覺)
    ART_MUSEUM = auto()  # 美術館
    GALLERY = auto()  # 商業藝廊

    # 3. 複合型場域 (重視休閒與體驗)
    CREATIVE_PARK = auto()  # 文創園區
    ART_VILLAGE = auto()  # 藝術村

    # 4. 展演與功能類
    EXPO_CENTER = auto()  # 展覽中心/中心
    PLATFORM = auto()  # 線上售票/資訊平台
