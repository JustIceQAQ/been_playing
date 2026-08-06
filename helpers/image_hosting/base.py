import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from helpers.crawler.proxy_helper import ProxyAdapter


class ImageHostingBase(abc.ABC):
    @abc.abstractmethod
    async def upload(
        self, image_url: str, proxies: "ProxyAdapter | None" = None, public_id: str | None = None, *args, **kwargs
    ) -> str | None:
        raise NotImplementedError
