import asyncio
import hashlib
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


async def get_cert_fingerprint(host: str, port: int = 443, timeout: float = 10.0) -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    reader, writer = await asyncio.wait_for(
        asyncio.open_connection(host, port, ssl=ctx, server_hostname=host),
        timeout=timeout,
    )
    try:
        der = writer.get_extra_info("ssl_object").getpeercert(binary_form=True)
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
    return hashlib.sha256(der).hexdigest()


async def should_skip_verify(host: str, trusted_fingerprints: set[str], port: int = 443) -> bool:
    trusted = {fp.lower().replace(":", "") for fp in trusted_fingerprints}
    try:
        fingerprint = await get_cert_fingerprint(host, port)
    except Exception:
        return False
    return fingerprint in trusted
