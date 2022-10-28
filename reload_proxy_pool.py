import abc
import asyncio
import base64
import dataclasses
import secrets

import dill
import httpx
from bs4 import BeautifulSoup

httpx_client = httpx.AsyncClient()


@dataclasses.dataclass
class Proxy:
    ip: str
    port: str
    protocol: str


class SourceInit(abc.ABC):
    ...


class freeProxySource(SourceInit):
    def __init__(self, filename="proxy.pkl"):
        self.root_path = ["http://free-proxy.cz/zh/proxylist/country/TW/all/ping/all"]
        self.filename = filename

    async def get_page_data(self, url, headers, httpx_client):
        response = await httpx_client.get(url, headers=headers)
        parsed = BeautifulSoup(response.text, "html5lib")
        return parsed.select_one("#proxy_list")

    def get_headers(self):
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/104.0.0.0 Safari/537.36"
            ),
            "Host": "free-proxy.cz",
            "Referer": "http://free-proxy.cz/zh/proxylist/country/TW/https/ping/all",
            "Content-Type": "Content-Type: text/html; charset=BIG5",
            "Cookie": f"fp={secrets.token_hex(16)}",
        }

    async def ip_availability(self, proxy: Proxy):
        target_url = "https://ncpi.ntmofa.gov.tw/visit.html"
        proxies = {
            f"{proxy.protocol}://".lower(): f"{proxy.protocol}://{proxy.ip}:{proxy.port}".lower()
        }
        try:
            async with httpx.AsyncClient(proxies=proxies) as client:
                response = await client.get(target_url, timeout=10)
                if response.status_code == 200:
                    return proxy
        except Exception as exc:
            print(exc)

    async def run(self):

        task = [
            self.get_page_data(url, self.get_headers(), httpx_client)
            for url in self.root_path
        ]

        all_data = await asyncio.gather(*task)

        tables = [
            [td.get_text() for td in tr.select("td:nth-child(n+1):nth-child(-n+3)")]
            for tr in all_data[0].select("tbody > tr")
        ]

        clean_data = []
        for data in tables:
            if data:
                s = data[0].index('("') + 2
                e = data[0].index('")')
                clean_data.append(
                    [base64.b64decode((data[0][s:e])).decode("utf-8"), data[1], data[2]]
                )

        proxies = [Proxy(*item) for item in clean_data]

        available_task = [self.ip_availability(p) for p in proxies]

        available_ip = await asyncio.gather(*available_task)

        clean_available_ip = [ip for ip in available_ip if ip]

        with open(self.filename, "wb") as f:
            dill.dump(clean_available_ip, f)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(freeProxySource().run())
