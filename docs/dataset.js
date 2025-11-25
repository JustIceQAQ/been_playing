const URL_SOURCE = "https://raw.githubusercontent.com/JustIceQAQ/been_playing/auto/data-update/data/v2/"

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


const platformTopicClass = [
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
    new Exhibition("CultureExpress", "文化快遞",
        new ButtonStyle("#fff", "#313131", "#313131")
    ),
    new Exhibition("GaCc", "中華文化總會",
        new ButtonStyle("#fff", "#7b0025", "#7b0025")
    )

]

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
    new Exhibition("n228mm", "二二八事件紀念基金會",
        new ButtonStyle("#fff", "#49b88d", "#c0d429")
    ),
    new Exhibition("HongGah", "鳳甲美術館",
        new ButtonStyle("#fff", "#585656", "#585656")
    ),
    new Exhibition("ShungYeArt", "順益台灣美術館",
        new ButtonStyle("#fff", "#83744c", "#585656")
    ),
    new Exhibition("PACT", "台北偶戲館",
        new ButtonStyle("#fff", "#e40012", "#db462f")),
    new Exhibition("Yatsen", "國立國父紀念館",
        new ButtonStyle("#fff", "#f6b64b", "#2f98d2")),
    new Exhibition("Nrm", "國家鐵道博物館",
        new ButtonStyle("#fff", "#009e40", "#fdfdfd")),
    new Exhibition("RedHouse", "西門紅樓",
        new ButtonStyle("#fff", "#c73405", "#c73405")),
    new Exhibition("YoChangArt", "有章藝術博物館",
        new ButtonStyle("#fff", "#585656", "#585656")
    ),
    new Exhibition("NTAEC", "國立台灣藝術教育館",
        new ButtonStyle("#fff", "#b83a32", "#24318e")
    ),

    new Exhibition("ChiPoLin", "齊柏林空間",
        new ButtonStyle("#fff", "#585656", "#585656")
    ),



    new Exhibition("kmoa", "基隆美術館",
        new ButtonStyle("#fff", "#e35449", "#e35449")
    ),

    new Exhibition("Culture435", "板橋435藝文特區",
        new ButtonStyle("#fff", "#e35449", "#e35449")
    ),




    new Exhibition("khm", "高雄市立歷史博物館",
        new ButtonStyle("#fff", "#e2007e", "#009fe7")
    ),
]

const allTopicClass = [].concat(exhibitionTopicClass, platformTopicClass)

const allTopicSet = new Set(allTopicClass.map((exhibition) => {
    return exhibition.topic
}))

const getInitTopic = () => {
    const params = new URLSearchParams(window.location.search);
    const topic = params.get('topic');
    if (topic === undefined || topic === null || !allTopicSet.has(topic)) {
        return allTopicClass[0].topic
    }
    return topic
}

const copyUrlToClipboard = (url) => {

    navigator.clipboard.writeText(url)
        .then(() => {
            const toastEl = document.getElementById('cpToast');
            if (toastEl) {
                const toast = new bootstrap.Toast(toastEl);
                toast.show();
            }
        })
        .catch((err) => {
            const toastEl = document.getElementById('cpToast');
            if (toastEl) {
                const toast = new bootstrap.Toast(toastEl);
                toast.show();
            }

        });
}

const customizeButtons = allTopicClass.map((exhibition) => {
    return {extend: exhibition.topic, className: `btn btn-${exhibition.topic}`}
})

const ACHIEVEMENTS_STORAGE_KEY = 'been-been-play-achievements';

const loadAchievements = () => {
    const raw = localStorage.getItem(ACHIEVEMENTS_STORAGE_KEY);
    try {
        return raw ? JSON.parse(raw) : [];
    } catch (e) {
        return [];
    }
};
const saveAchievements = (data) => {
    localStorage.setItem(ACHIEVEMENTS_STORAGE_KEY, JSON.stringify(data));
};

const getAchievementElement = (title, figure, uuid) => {
    const card = document.createElement('div');
    card.className = `card mb-3 bbp-${uuid}`;
    card.style.maxWidth = '540px';

    const row = document.createElement('div');
    row.className = 'row g-0';

    const colImg = document.createElement('div');
    colImg.className = 'col-md-4';
    const img = document.createElement('img');
    img.className = 'img-fluid rounded-start';
    img.src = figure;
    img.alt = title;
    colImg.appendChild(img);

    const titleEl = document.createElement('h5');
    titleEl.className = 'card-title';
    titleEl.textContent = title;

    const colText = document.createElement('div');
    colText.className = 'col-md-8';
    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    cardBody.appendChild(titleEl);
    colText.appendChild(cardBody)

    row.appendChild(colImg);
    row.appendChild(colText);
    card.appendChild(row);

    return card;
}

const addToAchievement = (title, figure, uuid, is_save = true) => {
    let element = getAchievementElement(title, figure)
    const container = document.getElementById('achievementList');
    if (container) {
        container.appendChild(element);
    }
    if (is_save) {
        const achievements = loadAchievements();
        const exists = achievements.some(item => item.uuid === uuid);
        if (!exists) {
            achievements.push({title, figure, uuid});
            saveAchievements(achievements);
        }
    }
}
const exportAchievementsToJSON = () => {
    const achievements = loadAchievements();
    const dataStr = JSON.stringify(achievements, null, 2);
    const blob = new Blob([dataStr], {type: "application/json"});
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = "achievements_backup.json";
    a.click();

    URL.revokeObjectURL(url);
}

let importedAchievementsData = null;

document.getElementById('importAchievementsInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        try {
            const data = JSON.parse(e.target.result);
            if (!Array.isArray(data)) {
                alert("格式錯誤：應為陣列！");
                return;
            }

            const isValid = data.every(item =>
                typeof item.title === "string" &&
                typeof item.figure === "string" &&
                typeof item.uuid === "string"
            );
            if (!isValid) {
                alert("格式錯誤：缺少必要欄位 (title, figure, UUID)");
                return;
            }

            importedAchievementsData = data;

            // 顯示 modal
            document.getElementById("importSummaryText").innerHTML =
                `你將匯入 <strong>${data.length}</strong> 筆成就資料，這將會覆蓋現有成就。確定嗎？`;

            const confirmModal = new bootstrap.Modal(document.getElementById('confirmImportModal'));
            confirmModal.show();
        } catch (err) {
            console.error(err);
            alert("匯入失敗：JSON 格式錯誤");
        }
    };
    reader.readAsText(file);
});

document.getElementById('btnConfirmImport').addEventListener('click', function () {
    if (importedAchievementsData) {
        localStorage.setItem(ACHIEVEMENTS_STORAGE_KEY, JSON.stringify(importedAchievementsData));
        alert("匯入成功！將重新載入頁面。");
        location.reload();
    }
});


document.getElementById('confirmDeleteAchievements').addEventListener('click', function () {
    // 清空 localStorage 中的成就資料
    localStorage.removeItem(ACHIEVEMENTS_STORAGE_KEY);

    const achievementList = document.getElementById('achievementList');
    achievementList.innerHTML = '';

    const deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteAllAchievementModal'));
    deleteModal.hide();

    const offcanvasAchievement = bootstrap.Offcanvas.getInstance(document.getElementById('offcanvasAchievement'));
    offcanvasAchievement.hide();
    location.reload();
});

allTopicClass.map((exhibition) => {
    $.fn.dataTable.ext.buttons[exhibition.topic] = {
        text: exhibition.name,
        action: function (e, dt, node, config) {
            dt.ajax.url(`${URL_SOURCE}${exhibition.topic}.json`).load()
        }
    }
})

const style = document.createElement('style');
style.type = 'text/css';

style.innerHTML = allTopicClass.map((exhibition) => {
    return `.btn-${exhibition.topic} {
    color:${exhibition.buttonStyle.color};
    background-color:${exhibition.buttonStyle.backgroundColor};
    border-color:${exhibition.buttonStyle.borderColor};
    --bs-btn-hover-color: ${exhibition.buttonStyle.color};
    --bs-btn-hover-bg: ${exhibition.buttonStyle.backgroundColor};
    }`
}).join(" ")
document.getElementsByTagName('head')[0].appendChild(style);
