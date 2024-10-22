import asyncio
import logging
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv

from configs.settings import get_settings
from exhibition.cksmh.re_script import CKSMHRunner
from helpers.cache.disk.helper import DiskCache
from helpers.image.imgur.helper import ImgurImage
from helpers.image.none.helper import NoneImage


async def main():
    runtime_setting = get_settings()

    # logging init
    logging.basicConfig(
        level=logging.DEBUG if runtime_setting.IS_DEBUG else logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

    if runtime_setting.IMGUR_API_CLIENT_ID:
        imgur = ImgurImage(client_id=runtime_setting.IMGUR_API_CLIENT_ID)
    else:
        imgur = NoneImage()
    disk_cache = DiskCache()

    all_async_script_runners = [
        CKSMHRunner().run(disk_cache, imgur),
    ]
    await asyncio.gather(*all_async_script_runners)


if __name__ == "__main__":
    # load local env file
    ROOT_DIR = Path(__file__).resolve(strict=True).parent
    this_env = ROOT_DIR / ".env"
    if this_env.exists():
        load_dotenv(this_env)

    runtime_setting = get_settings()
    SENTRY_SDK_DNS = (
        runtime_setting.SENTRY_SDK_DNS if not runtime_setting.IS_DEBUG else None
    )
    sentry_sdk.init(dsn=SENTRY_SDK_DNS, traces_sample_rate=1.0)
    asyncio.run(main())
