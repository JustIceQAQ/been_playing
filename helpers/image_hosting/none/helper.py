from typing import TYPE_CHECKING

from helpers.image_hosting.base import ImageHostingBase

if TYPE_CHECKING:
    from helpers.crawler.proxy_helper import TinyProxyAdapter


class NoneImageHosting(ImageHostingBase):
    async def upload(
        self, image_url: str, proxies: "TinyProxyAdapter | None" = None, public_id: str | None = None, *args, **kwargs
    ) -> str | None:
        return image_url


none_image_hosting = NoneImageHosting()
