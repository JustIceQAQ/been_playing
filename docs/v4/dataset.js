const URL_SOURCE = "https://raw.githubusercontent.com/JustIceQAQ/been_playing/auto/data-update/data/v2/";
const SOURCE_ROOT_URL = "https://raw.githubusercontent.com/JustIceQAQ/been_playing/auto/data-update/data/";

// venue(topic, name, textColor, bgColor, borderColor)
const v = (topic, name, c, bg, b) => ({ topic, name, c, bg, b: b ?? bg });

const venueGroups = [
    {
        region: "北台灣",
        subgroups: [
            {
                label: "台北 中正・大同・萬華",
                venues: [
                    v("CKSMH",       "中正紀念堂",               "#fff", "#04a1ae"),
                    v("Ntm",         "國立臺灣博物館",             "#fff", "#313131"),
                    v("Nmh",         "國立歷史博物館",             "#fff", "#8b3a47"),
                    v("NTCRI",       "國立台灣工藝研究發展中心",    "#fff", "#00d186"),
                    v("MuseumPost",  "郵政博物館",               "#fff", "#e6121c", "#12429c"),
                    v("NCPI",        "國家攝影文化中心",           "#fff", "#000001"),
                    v("n228mm",      "二二八事件紀念基金會",        "#fff", "#49b88d", "#c0d429"),
                    v("NTAEC",       "國立台灣藝術教育館",          "#fff", "#b83a32", "#24318e"),
                    v("AAAArchives", "國家發展委員會檔案管理局",    "#fff", "#00afa9", "#00192e"),
                    v("HuaShan1914", "華山1914文化創意產業園區",    "#fff", "#437321"),
                    v("MoCaTaipei",  "台北當代藝術館",             "#fff", "#E83434"),
                    v("TncMMM",      "臺灣新文化運動紀念館",        "#fff", "#9f211a"),
                    v("Nrm",         "國家鐵道博物館",             "#fff", "#009e40", "#fdfdfd"),
                    v("BoPiLiao",    "剝皮寮歷史街區",             "#fff", "#656565", "#cacaca"),
                    v("RedHouse",    "西門紅樓",                  "#fff", "#c73405"),
                    v("ArtistVillage","寶藏巖國際藝術村",          "#fff", "#5d7a3e"),
                    v("KiShuAn",     "紀州庵文學森林",             "#fff", "#6b5b3e"),
                    v("SoKaArt",     "索卡藝術中心",              "#fff", "#2c2c2c", "#777"),
                    v("XiZhiTang",   "羲之堂畫廊",               "#fff", "#8b6914"),
                ],
            },
            {
                label: "台北 中山・大安",
                venues: [
                    v("TFam",          "臺北市立美術館",   "#fff", "#2B2B2B"),
                    v("TaipeiExPoPark","花博公園",         "#fff", "#e52410", "#626468"),
                    v("Jam",           "忠泰美術館",       "#3c3d30", "#00d186"),
                    v("KingCarArt",    "金車文藝中心",     "#fff", "#000001"),
                    v("NTNUArtMuseum", "師大美術館",       "#fff", "#4d070b", "#000001"),
                    v("MoNTUE",        "北師美術館",       "#3c3d30", "#f0eb4c", "#4b4b4b"),
                    v("FuBonArtMuseum","富邦美術館",       "#fff", "#643164"),
                    v("Alien",         "金馬賓館當代美術館","#fff", "#1a4060"),
                    v("CG1839",        "1839 當代藝廊",   "#fff", "#2c3e50"),
                    v("WhiteStone",    "白石畫廊",         "#fff", "#555", "#888"),
                    v("MindSetArt",    "安卓藝術",         "#fff", "#333", "#666"),
                    v("CapitalArt",    "首都藝術中心",     "#fff", "#7d3c1a"),
                    v("Dac99",         "99度藝術中心",    "#fff", "#444", "#777"),
                    v("RuoMu",         "若木藝廊",         "#fff", "#5a7a5a"),
                    v("YiYun",         "異雲書屋",         "#fff", "#4a3728"),
                ],
            },
            {
                label: "台北 信義・松山・南港",
                venues: [
                    v("PACT",              "台北偶戲館",             "#fff", "#e40012", "#db462f"),
                    v("SongShanCulturalPark","松山文創園區",          "#fff", "#595758", "#F9DD00"),
                    v("CLab",              "台灣當代文化實驗場C-Lab", "#fff", "#f87065", "#f2f2f0"),
                    v("TwTc",              "台北世貿中心",            "#fff", "#ef5923"),
                    v("Yatsen",            "國立國父紀念館",           "#fff", "#f6b64b", "#2f98d2"),
                    v("ChiPoLin",          "齊柏林空間",              "#fff", "#585656"),
                    v("Tmc",               "台北流行音樂中心",         "#fff", "#FF5000", "#00BBD3"),
                    v("HistorySinica",     "中央研究院歷史文物陳列館", "#fff", "#8B4513"),
                    v("IOESinica",         "中央研究院民族學研究所博物館","#fff","#a0522d"),
                ],
            },
            {
                label: "台北 士林・北投",
                venues: [
                    v("Npm",         "國立故宮博物院",       "#fff", "#7D0000"),
                    v("NtSec",       "國立臺灣科學教育館",   "#3c3d30", "#FAA61A", "#33C0C4"),
                    v("ShungYeArt",  "順益台灣美術館",       "#fff", "#83744c", "#585656"),
                    v("KdMoFa",      "關渡美術館",           "#fff", "#eb7102"),
                    v("HongGah",     "鳳甲美術館",           "#fff", "#585656"),
                    v("YoChangArt",  "有章藝術博物館",       "#fff", "#585656"),
                    v("hkm",         "華岡博物館",           "#fff", "#4a235a"),
                ],
            },
            {
                label: "新北・基隆",
                venues: [
                    v("Mwr",         "世界宗教博物館",               "#fff", "#b01f23"),
                    v("NHRM",        "國家人權博物館",               "#fff", "#a42422", "#000001"),
                    v("NtcArtMuseum","新北市美術館",                  "#fff", "#000001"),
                    v("Culture435",  "板橋435藝文特區",              "#fff", "#e35449"),
                    v("NtcCeramics", "新北市立鶯歌陶瓷博物館",       "#fff", "#585656"),
                    v("JuMing",      "朱銘美術館",                   "#fff", "#8b7355"),
                    v("kmoa",        "基隆美術館",                   "#fff", "#e35449"),
                    v("OCAM",        "陽明海洋文化藝術館",            "#fff", "#b81d21"),
                ],
            },
            {
                label: "桃園",
                venues: [
                    v("TyCg", "桃園市立大溪木藝生態博物館", "#fff", "#7b5e2a"),
                ],
            },
            {
                label: "新竹",
                venues: [
                    v("nhclac", "國立新竹生活美學館", "#fff", "#2e7d62"),
                ],
            },
        ],
    },
    {
        region: "中台灣",
        subgroups: [
            {
                label: "台中",
                venues: [
                    v("NtMofa", "國立臺灣美術館",     "#fff", "#228b82"),
                    v("Mofia",  "臺中市纖維工藝博物館","#fff", "#3d7a9e"),
                ],
            },
            {
                label: "彰化",
                venues: [
                    v("chcsec", "國立彰化生活美學館", "#fff", "#2e7d62"),
                ],
            },
        ],
    },
    {
        region: "南台灣",
        subgroups: [
            {
                label: "嘉義",
                venues: [
                    v("ChiayiMM", "嘉義市立博物館", "#fff", "#228b82"),
                    v("ChiayiAM", "嘉義市立美術館", "#fff", "#313131"),
                ],
            },
            {
                label: "台南",
                venues: [
                    v("Tcm",        "臺南市立博物館",     "#fff", "#007f90"),
                    v("tncsec",     "國立臺南生活美學館", "#fff", "#313131"),
                    v("NMTL",       "國立臺灣文學館",     "#fff", "#5a4a1e"),
                    v("NMTH",       "國立臺灣歷史博物館", "#fff", "#a98d44"),
                    v("TnamMuseum", "臺南市美術館",       "#fff", "#228b82"),
                ],
            },
            {
                label: "高雄",
                venues: [
                    v("khm",   "高雄市立歷史博物館", "#fff", "#228b82"),
                    v("KmFa",  "高雄市立美術館",     "#fff", "#1a6b6b"),
                    v("Pier2", "駁2藝術特區",        "#fff", "#43748f"),
                ],
            },
        ],
    },
    {
        region: "東台灣",
        subgroups: [
            {
                label: "台東",
                venues: [
                    v("ttcsec", "國立臺東生活美學館", "#fff", "#4a7c59"),
                ],
            },
        ],
    },
    {
        region: "票務平台",
        subgroups: [
            {
                label: null,
                venues: [
                    v("KLook",          "KLook 客路",          "#fff",    "#fd5a01", "#e75234"),
                    v("BooksTickets",   "博客來售票網",          "#fff",    "#61C0B4"),
                    v("UdnFunLife",     "udn售票網",           "#fff",    "#F39800"),
                    v("OpenTix",        "OPENTIX兩廳院生活文化","#fff",    "#e75234"),
                    v("KKTix",          "KKTIX",              "#fff",    "#64be26"),
                    v("IBon",           "IBon",               "#8fc120", "#3f3a3a"),
                    v("KKDay",          "KKDay",              "#fff",    "#26bcc8"),
                    v("CultureExpress", "文化快遞",            "#fff",    "#313131"),
                    v("GaCc",           "中華文化總會",         "#fff",    "#7b0025"),
                    v("ArtEmperor",     "非池中藝術網",         "#fff",    "#e31472", "#f09500"),
                    v("NTT",            "新北市觀光旅遊網",     "#fff",    "#00c6fd"),
                    v("iCulture",       "iCulture 藝文資訊平台","#fff",   "#e85d26"),
                ],
            },
        ],
    },
];

const allVenues = venueGroups.flatMap(g => g.subgroups.flatMap(sg => sg.venues));
const allTopicSet = new Set(allVenues.map(v => v.topic));

const getInitTopic = () => {
    const topic = new URLSearchParams(window.location.search).get("topic");
    return topic && allTopicSet.has(topic) ? topic : allVenues[0].topic;
};

const copyUrlToClipboard = (url) => {
    navigator.clipboard.writeText(url).then(() => {
        const toastEl = document.getElementById("cpToast");
        if (toastEl) new bootstrap.Toast(toastEl).show();
    }).catch(() => {
        const toastEl = document.getElementById("cpToast");
        if (toastEl) new bootstrap.Toast(toastEl).show();
    });
};
