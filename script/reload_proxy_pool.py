import asyncio
import base64
import dataclasses
import datetime
import logging
import os
import secrets
from pathlib import Path

import dill
import httpx
import sentry_sdk
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv


@dataclasses.dataclass
class Proxy:
    ip: str
    port: str
    protocol: str


class FreeProxySource:
    def __init__(self, filename: str = "proxy.pkl"):
        self.root_path = ["http://free-proxy.cz/zh/proxylist/country/TW/all/ping/all"]
        self.filename = filename
        self.folder = Path(__file__).parent.absolute() / "fixture"

    def get_headers(self) -> dict:
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

    async def get_page_data(
        self, url: str, headers: dict, httpx_client: httpx.AsyncClient
    ) -> Tag:
        response = await httpx_client.get(url, headers=headers)
        parsed = BeautifulSoup(response.text, "html5lib")
        return parsed.select_one("#proxy_list")

    async def ip_availability(self, proxy: Proxy) -> Proxy | None:
        target_url = "https://www.google.com.tw/"
        proxies = {
            f"{proxy.protocol}://".lower(): f"{proxy.protocol}://{proxy.ip}:{proxy.port}".lower()
        }
        try:
            async with httpx.AsyncClient(proxies=proxies) as client:
                response = await client.get(target_url, timeout=10)
                if response.is_success:
                    return proxy
        except Exception as exc:
            logging.error(exc)
            return None

    async def run(self):
        async with httpx.AsyncClient(proxies=None) as httpx_client:

            tasks = [
                self.get_page_data(url, self.get_headers(), httpx_client)
                for url in self.root_path
            ]

            all_data = await asyncio.gather(*tasks)

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
                        [
                            base64.b64decode(data[0][s:e]).decode("utf-8"),
                            data[1],
                            data[2],
                        ]
                    )

        proxies = [Proxy(*item) for item in clean_data]

        available_task = [self.ip_availability(p) for p in proxies]

        available_ip = await asyncio.gather(*available_task)
        clean_available_ip = [ip for ip in available_ip if ip]

        with open(self.folder / self.filename, "wb") as f:
            timestamp = datetime.datetime.now().timestamp()
            dill.dump({"timestamp": timestamp, "available_ip": clean_available_ip}, f)


if __name__ == "__main__":
    # load local env file
    ROOT_DIR = Path(__file__).resolve(strict=True).parent
    this_env = ROOT_DIR / ".env"
    if this_env.exists():
        load_dotenv(this_env)

    # set sentry
    IS_DEBUG = os.getenv("IS_DEBUG", False)
    SENTRY_SDK_DNS = None if IS_DEBUG else os.getenv("SENTRY_SDK_DNS", None)
    sentry_sdk.init(dsn=SENTRY_SDK_DNS, traces_sample_rate=1.0)
    asyncio.run(FreeProxySource().run())
