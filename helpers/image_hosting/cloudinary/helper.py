import asyncio
import io

import cloudinary
import cloudinary.uploader
from PIL import Image
from rich.console import Console
from wreq import Proxy

from configs.settings import get_settings
from helpers.crawler.wreq.helper import WReqAsyncClient

_console = Console()
_MAX_FILE_SIZE = 10 * 1024 * 1024  # Cloudinary 免費方案上限 10MB
_WEBP_EXTS = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")
_COMPRESS_QUALITIES = (75, 55, 35)


def _compress_image(content: bytes, quality: int) -> bytes:
    with Image.open(io.BytesIO(content)) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return buf.getvalue()


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
            async with WReqAsyncClient(proxies=proxies) as client:
                response = await client.get(image_url)
                if not response.status.is_success():
                    _console.log(f"[red]Cloudinary Error: 下載圖片失敗（HTTP {response.status}）{image_url}[/red]")
                    return None
                return await response.bytes()
        except Exception as e:
            _console.log(f"[red]Cloudinary Error: 下載圖片失敗 {image_url} — {e}[/red]")
            return None

    async def upload(self, image_url: str) -> str | None:
        if not image_url:
            return None

        content = await self._download(image_url)
        if content is None:
            return None

        if len(content) > _MAX_FILE_SIZE:
            loop = asyncio.get_running_loop()
            for attempt, quality in enumerate(_COMPRESS_QUALITIES, start=1):
                compressed = await loop.run_in_executor(None, _compress_image, content, quality)
                _console.log(
                    f"[yellow]Cloudinary: 壓縮第 {attempt} 次（quality={quality}），{len(content)} → {len(compressed)} bytes[/yellow]"
                )
                content = compressed
                if len(content) <= _MAX_FILE_SIZE:
                    break
            else:
                _console.log(
                    f"[red]Cloudinary Error: 圖片過大（{len(content)} bytes），壓縮三次仍超限，略過 {image_url}[/red]"
                )
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
            _console.log(f"[red]Cloudinary Error: {e}[/red]")
            return None


async def main():
    settings = get_settings()
    cloud_name = settings.CLOUDINARY_CLOUD_NAME
    api_key = settings.CLOUDINARY_API_KEY
    api_secret = settings.CLOUDINARY_API_SECRET
    if cloud_name is None or api_key is None or api_secret is None:
        raise ValueError("Cloudinary 設定不完整，請確認環境變數")
    ci = CloudinaryImageHosting(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
    )
    result = await ci.upload(
        "https://svs.gsfc.nasa.gov/vis/a030000/a030800/a030877/frames/5760x3240_16x9_01p/BlackMarble_2016_1400m_africa_m_labeled.png"
    )
    _console.log(result)


if __name__ == "__main__":
    asyncio.run(main())
