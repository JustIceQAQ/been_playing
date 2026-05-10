class NoneImageHosting:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def upload(self, image_url: str) -> str | None:
        return image_url
