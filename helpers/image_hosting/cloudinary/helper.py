import asyncio
import io
from functools import lru_cache
from typing import TYPE_CHECKING, Literal

import cloudinary
import cloudinary.uploader
from PIL import Image
from rich.console import Console

from helpers.crawler.wreq.helper import WReqAsyncClient
from helpers.image_hosting.base import ImageHostingBase

if TYPE_CHECKING:
    from helpers.proxy_helper import ProxyAdapter

_console = Console()
_MAX_FILE_SIZE = 10 * 1024 * 1024  # Cloudinary 免費方案上限 10MB
_MAX_PIXELS = 400_000_000
_WEBP_EXTS = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")
_COMPRESS_QUALITIES = (75, 55, 35)


def _compress_image(content: bytes, quality: int) -> bytes:
    with Image.open(io.BytesIO(content)) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return buf.getvalue()


def _is_oversized_image(content: bytes) -> bool:
    """在不完整解壓的情況下，快速檢查圖片像素數是否過大。"""
    try:
        Image.MAX_IMAGE_PIXELS = None  # 暫時關閉，只為了讀 header
        with Image.open(io.BytesIO(content)) as img:
            w, h = img.size
            return w * h > _MAX_PIXELS
    except Exception:
        return False  # 讀不到就讓後面流程處理
    finally:
        Image.MAX_IMAGE_PIXELS = 178_956_970


class CloudinaryImageHosting(ImageHostingBase):
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        self.cloudinary = cloudinary
        self.cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True,
        )

    def _log(self, message: str, level: Literal["info", "warning", "error"] = "info"):
        if level == "error":
            _console.log(f"[red]Cloudinary Error: {message}[/red]")
        elif level == "warning":
            _console.log(f"[yellow]Cloudinary: {message}[/yellow]")
        else:
            _console.log(f"[green]Cloudinary: {message}[/green]")

    @property
    def loop(self):
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.get_event_loop()

    async def _download(self, image_url: str, proxies: "ProxyAdapter | None") -> bytes | None:
        try:
            if proxies is None:
                use_proxies = None
            else:
                use_proxies = proxies.to_wreq()
            async with WReqAsyncClient(proxies=use_proxies) as client:
                response = await client.get(image_url)
                if not response.status.is_success():
                    self._log("下載圖片失敗(HTTP {response.status}){image_url}", level="error")
                    return None
                return await response.bytes()
        except Exception:
            return None

    def _convert_to_webp(self, secure_url: str | None) -> str | None:
        if secure_url is None:
            return None
        for ext in _WEBP_EXTS:
            if secure_url.endswith(ext):
                return secure_url[: -len(ext)] + ".webp"
        return secure_url

    async def upload(
        self, image_url: str, proxies: "ProxyAdapter | None" = None, public_id: str | None = None, *args, **kwargs
    ) -> str | None:
        if not image_url:
            return None
        try:
            upload_result = await self.upload_from_url(image_url, public_id=public_id)
            if upload_result and "secure_url" in upload_result:
                secure_url = upload_result["secure_url"]
                return self._convert_to_webp(secure_url)
        except Exception:
            self._log("直接用 URL 上傳失敗，啟動下載重試機制... {image_url}", level="warning")

        content = await self._download(image_url, proxies)
        if content is None:
            return None

        needs_compress = len(content) > _MAX_FILE_SIZE
        if not needs_compress:
            needs_compress = await self.loop.run_in_executor(None, _is_oversized_image, content)

        if needs_compress:
            if len(content) > _MAX_FILE_SIZE:
                for attempt, quality in enumerate(_COMPRESS_QUALITIES, start=1):
                    compressed = await self.loop.run_in_executor(None, _compress_image, content, quality)
                    self._log(
                        f"壓縮第{attempt}次(quality={quality}), {len(content)} → {len(compressed)} bytes",
                        level="warning",
                    )
                    content = compressed
                    if len(content) <= _MAX_FILE_SIZE:
                        break
                else:
                    self._log("圖片過大（{len(content)} bytes)，壓縮三次仍超限，略過 {image_url}", level="error")
                    return None

        try:
            upload_result = await self.upload_from_file(content, public_id=public_id)
            secure_url: str = upload_result.get("secure_url", "")
            return self._convert_to_webp(secure_url)
        except Exception:
            return None

    async def upload_from_url(self, image_url: str, public_id: str | None = None):
        use_args = (image_url,)
        use_kwarg = {"resource_type": "image"}
        if public_id is not None:
            use_kwarg["public_id"] = public_id

        upload_result = await self.loop.run_in_executor(
            None,
            lambda: self.cloudinary.uploader.upload(*use_args, **use_kwarg),
        )
        return upload_result

    async def upload_from_file(self, image_file: bytes, public_id: str | None = None):
        use_args = (image_file,)
        use_kwarg = {"resource_type": "image"}
        if public_id is not None:
            use_kwarg["public_id"] = public_id
        upload_result = await self.loop.run_in_executor(
            None,
            lambda: self.cloudinary.uploader.upload(*use_args, **use_kwarg),
        )
        return upload_result

    async def destroy_from_public_id(self, public_id: str):
        destroy_result = await self.loop.run_in_executor(
            None,
            lambda: self.cloudinary.uploader.destroy(public_id),
        )
        return destroy_result


@lru_cache
def get_initialized_cloudinary_image_hosting(
    cloud_name: str | None, api_key: str | None, api_secret: str | None
) -> CloudinaryImageHosting:
    if cloud_name is None or api_key is None or api_secret is None:
        raise ValueError("Cloudinary 設定不完整，請確認環境變數")
    return CloudinaryImageHosting(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
    )
