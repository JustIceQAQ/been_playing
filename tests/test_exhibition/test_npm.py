import pathlib
from bs4 import BeautifulSoup

from app.exhibition.npm.parse import NpmPreviewParse
from helpers.storage.helper import ExhibitionItem


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
