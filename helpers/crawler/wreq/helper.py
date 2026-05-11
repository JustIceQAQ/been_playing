import wreq


class WReqAsyncClient:
    def __init__(self, *args, **kwargs) -> None:
        self.client = wreq.Client(
            *args,
            **kwargs,
            emulation=wreq.Emulation(profile=wreq.Profile.Firefox149),
            allow_redirects=True,
        )

    async def __aenter__(self) -> wreq.Client:
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
