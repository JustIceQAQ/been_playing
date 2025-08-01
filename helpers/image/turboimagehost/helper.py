import secrets

from bs4 import BeautifulSoup

from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import UA
from helpers.image.imgur.helper import limiter
from helpers.image.turboimagehost.schemas import Data, UploadResponse

headers = {
    "user-agent": UA.random,
    "referer": "https://www.turboimagehost.com/",
    "origin": "https://www.turboimagehost.com",
}
cookies = {"PHPSESSID": secrets.token_hex(16)}


class TurboImageHost:
    def __init__(self):
        self.url_upload = "https://s8d3.turboimagehost.com/remote_upload.tu?"

    @limiter.limit
    async def upload(
        self, images_url: str, import_client: HttpxAsyncClient | None = None
    ) -> UploadResponse:
        this_client = import_client or HttpxAsyncClient()
        async with this_client as client:
            response = await client.post(
                self.url_upload,
                follow_redirects=True,
                headers=headers,
                cookies=cookies,
                data={"images": images_url, "imcontent": "all", "thumb_size": 500},
            )
            response.raise_for_status()
        s = BeautifulSoup(response.content)
        img_code_ipms = s.select_one("#imgCodeIPMS")
        return UploadResponse(
            success=response.is_success,
            status=response.status_code,
            data=Data(webp_link=img_code_ipms.get("value").split("](")[1][:-1]),
        )
