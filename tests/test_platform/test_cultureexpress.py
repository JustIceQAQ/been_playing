import httpx
from helpers.headers_helper import generate_headers


def test_get_cultureexpress_data():
    headers = generate_headers(referer="https://cultureexpress.taipei")
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
