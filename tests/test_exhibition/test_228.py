import base64
import pathlib
import re

from pydantic import BaseModel
import pytest
import httpx
import json
from helpers.headers_helper import UA
from bs4 import BeautifulSoup
from urllib.parse import quote


@pytest.mark.asyncio
async def test_get_228_header():
    headers = {"user-agent": UA.random}
    async with httpx.AsyncClient(timeout=None, headers=headers) as client:
        response = await client.get("https://www.228.org.tw/exhibitionsnew")
    assert response.status_code == 200
    parsed = BeautifulSoup(response.text, "html5lib")
    find_all_result = parsed.find_all("script", {"type": "application/json"})
    assert len(find_all_result) == 5


def test_parsed_txt():
    raw_txt = pathlib.Path("fixtrue/_228_wix_viewer_model.json").read_text(
        encoding="utf-8"
    )
    wix_viewer_model_dict = json.loads(raw_txt)
    print(
        wix_viewer_model_dict["siteFeaturesConfigs"]["dynamicPages"][
            "prefixToRouterFetchData"
        ]["exhibitionse"]["optionsData"]["headers"]
    )


class CommonConfig(BaseModel):
    brand: str = "wix"
    host: str = "VIEWER"
    BSI: str
    siteRevision: str = "3128"
    renderingFlow: str = "NONE"
    language: str = "zh"
    locale: str = "zh-tw"

    def to_query(self) -> str:
        json_str = self.model_dump_json()
        return quote(json_str)


def query_p(app_id: str) -> str:
    return base64.b64encode(
        json.dumps(
            {
                "dataCollectionId": "Exhibitionsnew",
                "query": {
                    "filter": {},
                    "sort": [{"fieldName": "sortId", "order": "DESC"}],
                    "paging": {"offset": 0, "limit": 10},
                    "fields": [],
                },
                "referencedItemOptions": [],
                "returnTotalCount": True,
                "environment": "LIVE",
                "appId": app_id,
            }
        ).encode("utf-8")
    ).decode("utf-8")


def extract_exhibition_info(html: str):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text = re.sub(r"[（(][^）)]*[）)]", "", text)

    date_pattern = re.compile(r"展覽期間[:：]?\s*([^\n]+)", re.IGNORECASE)
    location_pattern = re.compile(
        r"(展覽地點|地點|地址)[:：]?\s*([^\n<]+)", re.IGNORECASE
    )

    def parse_date(text):
        date_matches = re.findall(r"(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})", text)
        return [f"{int(y):04d}-{int(m):02d}-{int(d):02d}" for y, m, d in date_matches]

    period_match = date_pattern.search(text)

    if period_match:
        dates = parse_date(period_match.group(1))
        start_date = dates[0] if len(dates) > 0 else ""
        end_date = dates[1] if len(dates) > 1 else ""
        period = f"{start_date} ~ {end_date}" if end_date else start_date
    else:
        period = None

    location = None
    location_match = location_pattern.search(text)
    if location_match:
        location_raw = location_match.group(2).strip()
        parts = re.split(r"[／/]", location_raw)
        parts = [p.replace("二二八國家紀念館", "").strip() for p in parts]
        location = next(
            (
                p
                for p in parts
                if "樓" in p or "展區" in p or "展示室" in p or "空間" in p
            ),
            "",
        )
        if not location and parts:
            location = parts[-1]

    result = {"展覽期間": period, "展覽地點": location}

    return result


@pytest.mark.asyncio
async def test_get_data():
    raw_txt = pathlib.Path("fixtrue/_228_wix_viewer_model.json").read_text(
        encoding="utf-8"
    )
    wix_viewer_model_dict = json.loads(raw_txt)
    headers_values = wix_viewer_model_dict["siteFeaturesConfigs"]["dynamicPages"][
        "prefixToRouterFetchData"
    ]["exhibitionse"]["optionsData"]["headers"]
    x_wix_grid_app_id = headers_values["x-wix-grid-app-id"]

    common_config = CommonConfig(BSI=x_wix_grid_app_id).to_query()
    r = query_p(x_wix_grid_app_id)
    headers = {
        "user-agent": UA.random,
        "referer": "https://www.228.org.tw/",
        "authorization": headers_values["Authorization"],
        "commonconfig": common_config,
    }
    async with httpx.AsyncClient(timeout=None, headers=headers) as client:
        response = await client.get(
            "https://www.228.org.tw/_api/cloud-data/v2/items/query", params={".r": r}
        )
        assert response.status_code == 200
        result = response.json()
        print()
        for item in result["dataItems"]:
            print(extract_exhibition_info(item["data"]["top_paragraph"]))
