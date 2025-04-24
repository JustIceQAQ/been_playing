import pathlib

import pytest

from app.exhibition.ntsec.format.address import get_page_address
from helpers.translation.beautiful_soup import BeautifulSoupTranslation

testdata = [
    (
        pathlib.Path("./fixtrue/5688.html"),
        "國立臺灣科學教育館7樓西側特展區",
    ),
    (
        pathlib.Path("./fixtrue/5531.html"),
        "本館3樓西側特展廳",
    ),
    (
        pathlib.Path("./fixtrue/5462.html"),
        "本館4樓東側展區",
    ),
    (
        pathlib.Path("./fixtrue/5653.html"),
        "本館七樓東側特展廳",
    ),
    (
        pathlib.Path("./fixtrue/3226.html"),
        "本館8樓扇形廣場",
    ),
]


@pytest.mark.parametrize("html_path,address", testdata)
def test_get_page_address(html_path: pathlib.Path, address: str):
    soup = BeautifulSoupTranslation().load_file_to_object(html_path)
    result = get_page_address(soup)
    assert result == address
