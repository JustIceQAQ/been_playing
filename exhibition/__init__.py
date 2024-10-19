import dataclasses
import enum


@dataclasses.dataclass
class ExhibitionInformation:
    fullname: str = None
    code_name: str = None
    external_link: str = None


class ExhibitionEnum(ExhibitionInformation, enum.Enum):
    HuaShan1914 = (
        "華山1914文化創意產業園區",
        "huashan1914",
        "https://www.huashan1914.com/w/huashan1914/exhibition",
    )
    CKSMH = (
        "中正紀念堂",
        "cksmh",
        "https://www.cksmh.gov.tw/activitysoonlist_369.html",
    )
    MocaTaipei = (
        "台北當代藝術館",
        "mocataipei",
        "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent",
    )
    NPM = (
        "國立故宮博物院",
        "npm",
        "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1",
    )
    SongShanCulturalPark = (
        "松山文創園區",
        "songshanculturalpark",
        "https://www.songshanculturalpark.org/exhibition",
    )
    NTSEC = (
        "國立臺灣科學教育館",
        "ntsec",
        "https://www.ntsec.gov.tw/article/list.aspx?a=25",
    )
    TFAM = (
        "臺北市立美術館",
        "tfam",
        "https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
    )
    TicketsUdnFunLife = (
        "udn售票網",
        "tickets_udnfunlife",
        "https://tickets.udnfunlife.com/application/UTK01/UTK0101_.aspx/GET_PUSH_LIST",
    )
    TicketsBooks = (
        "博客來售票網",
        "tickets_books",
        "https://tickets.books.com.tw/leisure/",
    )
    NTM = (
        "國立臺灣博物館",
        "ntm",
        "https://www.ntm.gov.tw/submenu_178.html",
    )
    TMC = (
        "台北流行音樂中心",
        "tmc",
        "https://www.tmc.taipei/tw/lastest-event",
    )
    NMH = (
        "國立歷史博物館",
        "nmh",
        "https://www.nmh.gov.tw/activitysoonlist_66.html",
    )
    TWTC = (
        "台北世貿中心",
        "twtc",
        "https://twtc.com.tw/exhibition?p=home",
    )
    MWR = (
        "世界宗教博物館",
        "mwr",
        "https://www.mwr.org.tw/xcpmtexhi?xsmsid=0H305740978429024070",
    )
    MuseumPost = (
        "郵政博物館",
        "museum_post",
        "https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage=1",
    )
    Jam = (
        "忠泰美術館",
        "jam",
        "http://jam.jutfoundation.org.tw/online-exhibition",
    )
    NCPI = (
        "國家攝影文化中心",
        "ncpi",
        "https://ncpi.ntmofa.gov.tw/News_OnlineExhibitionPic_str.aspx?n=8006&sms=15632",
    )
    NTCArtMuseum = (
        "新北市美術館",
        "ntc_art_museum",
        "https://ntcart.museum/exhibition",
    )

    OpenTix = (
        "OPENTIX兩廳院生活文化",
        "opentix",
        "https://www.opentix.life/search/%20/ABOUT_TO_BEGIN?category=%E5%B1%95%E8%A6%BDAll",
    )
    KLook = (
        "KLOOK客路",
        "klook",
        "https://www.klook.com/zh-TW/event/city-mcate/19-3-taipei-convention-exhibition-tickets/",
    )

    KKTix = (
        "KKTix",
        "KKTix",
        "https://kktix.com/events?category_id=11",
    )

    IBon = (
        "ibon售票",
        "ibon",
        "https://tour.ibon.com.tw/home/search?category=exhibition",
    )

    KKDay = (
        "KKDay",
        "KKDay",
        "https://www.kkday.com/zh-tw/country/taiwan/events-and-exhibitions?sort=prec&page=1",
    )

    FuBonArtMuseum = (
        "FuBonArtMuseum",
        "FuBonArtMuseum",
        "https://www.fubonartmuseum.org/Default",
    )
    CLab = (
        "台灣當代文化實驗場C-Lab",
        "CLab",
        "https://clab.org.tw/events/",
    )

    BUG = (
        "BUG",
        "BUG",
        "BUG",
    )
