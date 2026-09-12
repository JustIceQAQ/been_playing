import pathlib
import ssl
from functools import lru_cache

import certifi

from configs.settings import get_settings


class SSLContextAdapter:
    def __init__(self, twca_intermediate_path: pathlib.Path):
        self.twca_intermediate = twca_intermediate_path

        certifi_bundle = pathlib.Path(certifi.where()).read_text(encoding="utf-8")
        twca_intermediate_text = self.twca_intermediate.read_text(encoding="utf-8")
        self._bundle = twca_intermediate_text + "\n" + certifi_bundle

    def to_httpx(self) -> ssl.SSLContext:
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(cadata=self._bundle)
        return ssl_context

    def to_niquests(self) -> str:
        return self._bundle


@lru_cache(maxsize=1)
def get_ssl_context() -> SSLContextAdapter:
    runtime_settings = get_settings()
    return SSLContextAdapter(runtime_settings.FIXTURE_PATH / "twca_intermediate.pem")
