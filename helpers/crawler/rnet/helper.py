import rnet


class RNetAsyncClient:
    def __init__(self, *args, **kwargs) -> None:
        self.client = rnet.Client(impersonate=rnet.Impersonate.Firefox139)
        self.args = args
        self.kwargs = kwargs

    async def __aenter__(self) -> rnet.Client:
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
