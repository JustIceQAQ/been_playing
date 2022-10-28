import abc
import dataclasses
import random
from pathlib import Path
from typing import List

import dill


class ProxyInit(abc.ABC):
    proxy_pool = None

    @abc.abstractmethod
    def get_random_proxy(self):
        raise NotImplementedError

    @abc.abstractmethod
    def load_source(self):
        raise NotImplementedError


@dataclasses.dataclass
class Proxy:
    ip: str
    port: str
    protocol: str


class FreeProxy(ProxyInit):
    def get_random_proxy(self):
        runtime_proxy = random.choice(self.proxy_pool)
        return {
            runtime_proxy.protocol.lower(): f"{runtime_proxy.ip}:{runtime_proxy.port}"
        }

    def load_source(self, path="proxy.pkl"):
        proxy_path = Path(path)
        if proxy_path.is_file():
            with open(proxy_path, "rb") as f:
                self.proxy_pool: List[Proxy] = dill.load(f)
        else:
            raise FileNotFoundError("Not Find proxy.pkl")


class NoneProxy(ProxyInit):
    def get_random_proxy(self):
        return self.proxy_pool

    def load_source(self):
        return None


if __name__ == "__main__":
    fp = FreeProxy()
    fp.load_source(path="../proxy.pkl")
    print(fp.get_random_proxy())
