import rnet


class RNetAsyncClient:
    def __init__(self, *args, **kwargs) -> None:
        self.client = rnet.Client(*args, **kwargs, impersonate=rnet.Impersonate.OkHttp5)

    async def __aenter__(self) -> rnet.Client:
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
