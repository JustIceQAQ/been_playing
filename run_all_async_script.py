import asyncio
import logging
import os
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv

from exhibition.cksmh.re_script import CKSMHRunner
from helpers.cache.disk.helper import DiskCache
from helpers.image.imgur.helper import ImgurImage


async def main():
    # check env values
    IS_DEBUG = os.getenv("IS_DEBUG", False)
    CLIENT_ID = os.getenv("IMGUR_API_CLIENT_ID", False)
    CLIENT_SECRET = os.getenv("IMGUR_API_CLIENT_SECRET", False)

    # logging init
    logging.basicConfig(
        level=logging.DEBUG if IS_DEBUG else logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

    if CLIENT_ID and CLIENT_SECRET:
        imgur = ImgurImage(client_id=CLIENT_ID)
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

    # set sentry
    IS_DEBUG = os.getenv("IS_DEBUG", False)
    SENTRY_SDK_DNS = os.getenv("SENTRY_SDK_DNS", None) if not IS_DEBUG else None

    sentry_sdk.init(dsn=SENTRY_SDK_DNS, traces_sample_rate=1.0)
    asyncio.run(main())
