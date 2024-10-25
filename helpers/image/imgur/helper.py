import httpx

from helpers.image.imgur.limiter import AsyncLimiter
from helpers.image.imgur.schemas import UploadResponse

limiter = AsyncLimiter(delay=8)


class ImgurImage:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, client_id: str | None = None, client: httpx.AsyncClient | None = None
    ):
        self.client = client or httpx.AsyncClient(timeout=None)
        self._header: dict = {"Authorization": f"Client-ID {client_id}"}

    def authorization_exist(self, is_raise=True) -> bool:
        if self._header is None:
            if is_raise:
                raise ValueError("Authorization is not set, please run .login")
            return False
        return True

    @limiter.limit
    async def upload(self, image_url: str) -> UploadResponse:
        self.authorization_exist()
        data = {
            "image": image_url,
            "type": "url",
        }
        response = await self.client.post(
            "https://api.imgur.com/3/image", data=data, headers=self._header
        )
        return UploadResponse.model_validate(response.json())

    async def close(self):
        await self.client.aclose()
