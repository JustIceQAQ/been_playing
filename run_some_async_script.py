import argparse
import asyncio
import logging
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv

from app.museums.khm import KhmRunner
from configs.settings import get_settings
from helpers.cache import DiskCache, NoneCache
from helpers.crawler.scraper.helper import available_scraper_async_client
from helpers.image.none.helper import NoneImage
from helpers.image.turboimagehost.helper import TurboImageHost


async def main(worker: int | None = None, worker_max: int | None = None):
    runtime_setting = get_settings()

    # logging init
    logging.basicConfig(
        level=logging.DEBUG if runtime_setting.IS_DEBUG else logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

    if runtime_setting.IS_DEBUG:
        imgur = NoneImage()
    else:
        imgur = TurboImageHost()

    disk_cache = NoneCache() if runtime_setting.IS_DEBUG else DiskCache()
    job = [KhmRunner]
    script_total = len(job)
    prefix = None
    if (worker is not None) and (worker_max is not None) and (worker_max > 0):
        chunk_size = (script_total + worker_max - 1) // worker_max
        start = (worker - 1) * chunk_size
        end = min(start + chunk_size, script_total)
        scripts_to_run = job[start:end]
        prefix = f"worker_{worker}"
    else:
        scripts_to_run = job

    await available_scraper_async_client(runtime_setting.SCRAPER_API_KEY)

    all_async_script_runners = [
        RunnerObj().run(disk_cache, imgur, prefix, develop_mode=True)
        for RunnerObj in scripts_to_run
    ]
    await asyncio.gather(*all_async_script_runners, return_exceptions=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=False, default=None)
    parser.add_argument("--max-worker", type=int, required=False, default=None)
    args = parser.parse_args()

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
    # asyncio.run(main(args.worker, args.max_worker))
