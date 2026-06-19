import httpxyz as httpx
from wreq import Proxy


class ProxyAdapter:
    def __init__(self, proxy_url: str | None):
        self.proxy_url = proxy_url

    def to_httpx(self) -> httpx.Proxy:
        return httpx.Proxy(url=self.proxy_url)

    def to_niquests(self) -> dict:
        return {"http": self.proxy_url, "https": self.proxy_url}

    def to_wreq(self) -> list[Proxy] | None:
        proxies = None if self.proxy_url is None else [Proxy.all(self.proxy_url)]
        return proxies
