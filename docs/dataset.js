const URL_SOURCE = "https://raw.githubusercontent.com/JustIceQAQ/been_playing/deploy/data/v2/"
// const URL_SOURCE = "https://raw.githubusercontent.com/JustIceQAQ/been_playing/refs/heads/develop/data/v2/"

class Exhibition {
    constructor(topic, name, buttonStyle) {
        this.topic = topic;
        this.name = name;
        this.buttonStyle = buttonStyle
    }
}

class ButtonStyle {
    constructor(color, backgroundColor, borderColor) {
        this.color = color;
        this.backgroundColor = backgroundColor;
        this.borderColor = borderColor;
    }
}

const exhibitionTopicClass = [
    new Exhibition("HuaShan1914", "華山1914文化創意產業園區",
        new ButtonStyle("#fff", "#437321", "#437321")
    ),
    new Exhibition("MoCaTaipei", "台北當代藝術館",
        new ButtonStyle("#fff", "#E83434", "#E83434")
    ),
    new Exhibition("CKSMH", "中正紀念堂",
        new ButtonStyle("#fff", "#04a1ae", "#04a1ae")
    ),
    new Exhibition("Npm", "國立故宮博物院",
        new ButtonStyle("#fff", "#7D0000", "#7D0000")
    ),
    new Exhibition("Ntm", "國立臺灣博物館",
        new ButtonStyle("#fff", "#313131", "#313131")
    ),
    new Exhibition("NtSec", "國立臺灣科學教育館",
        new ButtonStyle("#3c3d30", "#FAA61A", "#33C0C4")
    ),
    new Exhibition("SongShanCulturalPark", "松山文創園區",
        new ButtonStyle("#fff", "#595758", "#F9DD00")
    ),
    new Exhibition("TFam", "臺北市立美術館",
        new ButtonStyle("#fff", "#2B2B2B", "#2B2B2B")
    ),
    new Exhibition("Tmc", "台北流行音樂中心",
        new ButtonStyle("#fff", "#FF5000", "#00BBD3")
    ),
    new Exhibition("Nmh", "國立歷史博物館",
        new ButtonStyle("#fff", "#8b3a47", "#8b3a47")
    ),
    new Exhibition("NTCRI", "國立台灣工藝研究發展中心",
        new ButtonStyle("#fff", "#00d186", "#00d186")
    ),
    new Exhibition("TwTc", "台北世貿中心",
        new ButtonStyle("#fff", "#ef5923", "#ef5923")
    ),
    new Exhibition("Mwr", "世界宗教博物館",
        new ButtonStyle("#fff", "#b01f23", "#b01f23")
    ),
    new Exhibition("MuseumPost", "郵政博物館",
        new ButtonStyle("#fff", "#e6121c", "#12429c")
    ),
    new Exhibition("Jam", "忠泰美術館",
        new ButtonStyle("#3c3d30", "#00d186", "#00d186")
    ),
    new Exhibition("NCPI", "國家攝影文化中心",
        new ButtonStyle("#fff", "#000001", "#000001")
    ),
    new Exhibition("NtcArtMuseum", "新北市美術館",
        new ButtonStyle("#fff", "#000001", "#000001")
    ),
    new Exhibition("KLook", "KLook 客路",
        new ButtonStyle("#fff", "#fd5a01", "#e75234")
    ),
    new Exhibition("BooksTickets", "博客來售票網",
        new ButtonStyle("#fff", "#61C0B4", "#61C0B4")
    ),
    new Exhibition("UdnFunLife", "udn售票網",
        new ButtonStyle("#fff", "#F39800", "#F39800")
    ),
    new Exhibition("OpenTix", "OPENTIX兩廳院生活文化",
        new ButtonStyle("#fff", "#e75234", "#e75234")
    ),
    new Exhibition("KKTix", "KKTIX",
        new ButtonStyle("#fff", "#64be26", "#64be26")
    ),
    new Exhibition("IBon", "IBon",
        new ButtonStyle("#8fc120", "#3f3a3a", "#3f3a3a")
    ),
    new Exhibition("KKDay", "KKDay",
        new ButtonStyle("#fff", "#26bcc8", "#26bcc8")
    ),
    new Exhibition("FuBonArtMuseum", "富邦美術館",
        new ButtonStyle("#fff", "#643164", "#643164")
    ),
    new Exhibition("CLab", "台灣當代文化實驗場C-Lab",
        new ButtonStyle("#fff", "#f87065", "#f2f2f0")
    ),
    new Exhibition("KingCarArt", "金車文藝中心",
        new ButtonStyle("#fff", "#000001", "#000001")
    ),
    new Exhibition("BoPiLiao", "剝皮寮歷史街區",
        new ButtonStyle("#fff", "#656565", "#cacaca")
    ),
    new Exhibition("NTNUArtMuseum", "師大美術館",
        new ButtonStyle("#fff", "#4d070b", "#000001")
    ),
    new Exhibition("NHRM", "國家人權博物館",
        new ButtonStyle("#fff", "#a42422", "#000001")
    ),
    new Exhibition("TaipeiExPoPark", "花博公園",
        new ButtonStyle("#fff", "#e52410", "#626468")
    ),
    new Exhibition("OCAM", "陽明海洋文化藝術館",
        new ButtonStyle("#fff", "#b81d21", "#b81d21")
    ),
    new Exhibition("TncMMM", "臺灣新文化運動紀念館",
        new ButtonStyle("#fff", "#9f211a", "#9f211a")
    ),
    new Exhibition("KdMoFa", "關渡美術館",
        new ButtonStyle("#fff", "#eb7102", "#eb7102")
    ),

]


const customizeButtons = exhibitionTopicClass.map((exhibition) => {
    return {extend: exhibition.topic, className: `btn btn-${exhibition.topic}`}
})


exhibitionTopicClass.map((exhibition) => {
    $.fn.dataTable.ext.buttons[exhibition.topic] = {
        text: exhibition.name,
        action: function (e, dt, node, config) {
            console.log(`${URL_SOURCE}${exhibition.topic}.json`)
            dt.ajax.url(`${URL_SOURCE}${exhibition.topic}.json`).load()
        }
    }
})

const style = document.createElement('style');
style.type = 'text/css';

style.innerHTML = exhibitionTopicClass.map((exhibition) => {
    return `.btn-${exhibition.topic} {
    color:${exhibition.buttonStyle.color};
    background-color:${exhibition.buttonStyle.backgroundColor};
    border-color:${exhibition.buttonStyle.borderColor};
    --bs-btn-hover-color: ${exhibition.buttonStyle.color};
    --bs-btn-hover-bg: ${exhibition.buttonStyle.backgroundColor};
    }`
}).join(" ")
document.getElementsByTagName('head')[0].appendChild(style);




