import dataclasses
import enum


@dataclasses.dataclass
class ExhibitionInformation:
    fullname: str = None
    code_name: str = None


class ExhibitionEnum(ExhibitionInformation, enum.Enum):
    huashan1914 = (
        "華山1914文化創意產業園區",
        "huashan1914",
    )
    cksmh = (
        "中正紀念堂",
        "cksmh",
    )
    mocataipei = (
        "台北當代藝術館",
        "mocataipei",
    )
    npm = (
        "國立故宮博物院",
        "npm",
    )
    songshanculturalpark = (
        "松山文創園區",
        "songshanculturalpark",
    )
    ntsec = (
        "國立臺灣科學教育館",
        "ntsec",
    )
    tfam = (
        "臺北市立美術館",
        "tfam",
    )
    tickets_udnfunlife = (
        "udn售票網",
        "tickets_udnfunlife",
    )
    tickets_books = (
        "博客來售票網",
        "tickets_books",
    )
    ntm = (
        "國立臺灣博物館",
        "ntm",
    )
    tmc = (
        "台北流行音樂中心",
        "tmc",
    )
