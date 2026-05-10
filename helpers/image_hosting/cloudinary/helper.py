import asyncio

import cloudinary
import cloudinary.uploader
from rnet import Proxy

from configs.settings import get_settings
from helpers.crawler.rnet.helper import RNetAsyncClient

_MAX_FILE_SIZE = 10 * 1024 * 1024  # Cloudinary 免費方案上限 10MB
_WEBP_EXTS = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")


class CloudinaryImageHosting:
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        self.cloudinary = cloudinary
        self.cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True,
        )

    async def _download(self, image_url: str) -> bytes | None:
        settings = get_settings()
        proxies = None if settings.PROXY_POOL is None else [Proxy.all(settings.PROXY_POOL)]
        try:
            async with RNetAsyncClient(proxies=proxies) as client:
                response = await client.get(image_url)
                if not response.status_code.is_success():
                    print(f"Cloudinary Error: 下載圖片失敗（HTTP {response.status_code}）{image_url}")
                    return None
                return await response.bytes()
        except Exception as e:
            print(f"Cloudinary Error: 下載圖片失敗 {image_url} — {e}")
            return None

    async def upload(self, image_url: str) -> str | None:
        if not image_url:
            return None

        content = await self._download(image_url)
        if content is None:
            return None

        if len(content) > _MAX_FILE_SIZE:
            print(f"Cloudinary Error: 圖片過大（{len(content)} bytes），略過 {image_url}")
            return None

        loop = asyncio.get_running_loop()
        try:
            upload_result = await loop.run_in_executor(
                None,
                lambda: self.cloudinary.uploader.upload(content, resource_type="image"),
            )
            secure_url: str = upload_result.get("secure_url", "")
            for ext in _WEBP_EXTS:
                if secure_url.endswith(ext):
                    secure_url = secure_url[: -len(ext)] + ".webp"
                    break
            return secure_url or None
        except Exception as e:
            print(f"Cloudinary Error: {e}")
            return None


async def main():
    ci = CloudinaryImageHosting("dpoo988ui", "185848834645339", "fRuBzXslmWuH7cK5vDplHVHJih0")
    result = await ci.upload("https://khm.org.tw/storage/files/2635/original/9623291736620dc3a1d2e53.png")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
