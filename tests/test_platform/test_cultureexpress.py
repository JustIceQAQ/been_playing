import httpx
from helpers.headers_helper import get_header


def test_get_cultureexpress_data():
    headers = {
        **get_header(),
        "referer": "https://cultureexpress.taipei",
    }
    with httpx.Client(headers=headers) as client:
        response1 = client.get(
            url="https://cultureexpress.taipei/Event/C000003", headers=headers
        )
        response1.raise_for_status()

        response = httpx.get(
            "https://cultureexpress.taipei/Event/C000003",
            params={
                "CategoryID": "b89f200f-61e0-4956-9c2e-c90d5285ac67",
                "DateRange": 0,
                "PageIndex": 1,
            },
        )
        with open("cultureexpress.html", "b+w") as f:
            f.write(response.content)
