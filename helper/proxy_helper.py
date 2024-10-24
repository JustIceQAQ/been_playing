import abc
import dataclasses
import random
from pathlib import Path

import dill


@dataclasses.dataclass
class Proxy:
    ip: str
    port: str
    protocol: str


class ProxyInit(abc.ABC):
    proxy_pool: list[Proxy] | None = None

    @abc.abstractmethod
    def get_random_proxy(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def load_source(self, *args, **kwargs):
        raise NotImplementedError


class NoneProxy(ProxyInit):
    def get_random_proxy(self):
        return self.proxy_pool

    def load_source(self):
        return None


class FreeProxy(ProxyInit):
    def get_random_proxy(self):
        if self.proxy_pool is None:
            return self.proxy_pool

        runtime_proxy = random.choice(self.proxy_pool)
        return {
            runtime_proxy.protocol.lower(): f"{runtime_proxy.ip}:{runtime_proxy.port}"
        }

    def load_source(
        self,
        proxy_path: Path = Path(__file__).parent.parent.absolute()
        / "fixture"
        / "proxy.pkl",
    ):
        if proxy_path.is_file():
            with open(proxy_path, "rb") as f:
                data = dill.load(f)
                self.proxy_pool: list[Proxy] = data.get("available_ip")
        else:
            print("Not Find proxy.pkl. using NoneProxy")


if __name__ == "__main__":
    fp = FreeProxy()
    fp.load_source(
        proxy_path=Path(__file__).parent.parent.absolute() / "fixture" / "proxy.pkl"
    )
    print(fp.get_random_proxy())
