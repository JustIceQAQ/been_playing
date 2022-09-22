import dataclasses
import enum


@dataclasses.dataclass
class ExhibitionInformation:
    fullname: str = None
    code_name: str = None
    external_link: str = None


class ExhibitionEnum(ExhibitionInformation, enum.Enum):
    huashan1914 = (
        "華山1914文化創意產業園區",
        "huashan1914",
        "https://www.huashan1914.com/w/huashan1914/exhibition",
    )
    cksmh = (
        "中正紀念堂",
        "cksmh",
        "https://www.cksmh.gov.tw/activitysoonlist_369.html",
    )
    mocataipei = (
        "台北當代藝術館",
        "mocataipei",
        "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent",
    )
    npm = (
        "國立故宮博物院",
        "npm",
        "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1",
    )
    songshanculturalpark = (
        "松山文創園區",
        "songshanculturalpark",
        "https://www.songshanculturalpark.org/exhibition",
    )
    ntsec = (
        "國立臺灣科學教育館",
        "ntsec",
        "https://www.ntsec.gov.tw/User/Exhibitions.aspx?a=44",
    )
    tfam = (
        "臺北市立美術館",
        "tfam",
        "https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
    )
    tickets_udnfunlife = (
        "udn售票網",
        "tickets_udnfunlife",
        "https://tickets.udnfunlife.com/application/UTK01/UTK0101_.aspx/GET_PUSH_LIST",
    )
    tickets_books = (
        "博客來售票網",
        "tickets_books",
        "https://tickets.books.com.tw/leisure/",
    )
    ntm = (
        "國立臺灣博物館",
        "ntm",
        "https://www.ntm.gov.tw/submenu_178.html",
    )
    tmc = (
        "台北流行音樂中心",
        "tmc",
        "https://tmc.taipei/show/event/",
    )
    nmh = (
        "國立歷史博物館",
        "nmh",
        "https://www.nmh.gov.tw/activitysoonlist_66.html",
    )
    twtc = (
        "台北世貿中心",
        "twtc",
        "https://twtc.com.tw/exhibition?p=home",
    )
    mwr = (
        "世界宗教博物館",
        "mwr",
        "https://www.mwr.org.tw/xcpmtexhi?xsmsid=0H305740978429024070",
    )
    museum_post = (
        "郵政博物館",
        "museum_post",
        "https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage=1",
    )
