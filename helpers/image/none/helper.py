from .schemas import Data, UploadResponse


class NoneImage:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def upload(self, image_url: str) -> UploadResponse:
        return UploadResponse(success=True, status=200, data=Data(webp_link=image_url))
