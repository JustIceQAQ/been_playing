import pathlib

import pytest
from bs4 import BeautifulSoup
import httpx
from app.exhibition.npm.parse import NpmPreviewParse
from helpers.storage.helper import ExhibitionItem


@pytest.mark.asyncio
async def test_npm_url():
    url = "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1"
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.get(url)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)


def test_npm_preview_parse():
    html = pathlib.Path("./fixtrue/npm.gov.twExhibition-Preview.html").read_text(
        encoding="utf-8"
    )
    soup = BeautifulSoup(html, "html5lib")
    preview_parsed = soup.select("li.mb-8 > a.card.card-height-md")
    results = []
    for item in preview_parsed:
        results.append(
            NpmPreviewParse(item).parse_to_base_model(
                ExhibitionItem, target_domain="https://www.npm.gov.tw/"
            )
        )

    assert results
    assert len(results) == 3
