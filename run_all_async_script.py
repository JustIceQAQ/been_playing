import argparse
import asyncio
import orjson
import logging
from pathlib import Path
import aiofiles
import sentry_sdk
from dotenv import load_dotenv

from app.script import ALL_RUNNERS
from configs.settings import get_settings
from helpers.cache import DiskCache, NoneCache
from helpers.storage.helper import (
    Information,
    Coordinate,
    orjson_default_handler,
    last_week_update,
)
from helpers.crawler.scraper.helper import available_scraper_async_client
from helpers.image.none.helper import NoneImage
from helpers.image.turboimagehost.helper import TurboImageHost

ROOT_PATH = Path(__file__).parent.absolute()


async def generate_location(information: list["Information"]):
    ok_centers = []

    for location in information:
        fullname = location.fullname
        if isinstance(location.branch_coordinates, Coordinate):
            ok_centers.append(
                {
                    "fullname": fullname,
                    "latitude": location.branch_coordinates.latitude,
                    "longitude": location.branch_coordinates.longitude,
                    "venue_type": location.venue_type,
                    "external_link": location.external_link,
                }
            )
            continue
        if isinstance(location.branch_coordinates, list):
            for branch_coordinate in location.branch_coordinates:
                name = "None" if (this_name := branch_coordinate.name) is None else this_name
                ok_centers.append(
                    {
                        "fullname": fullname + "-" + name,
                        "latitude": branch_coordinate.latitude,
                        "longitude": branch_coordinate.longitude,
                        "venue_type": location.venue_type,
                        "external_link": location.external_link,
                    }
                )
            continue
        if location.branch_coordinates is None:
            pass

    async with aiofiles.open(ROOT_PATH / "data" / "v2" / "_ALL_LOCATION.json", "wb+") as afp:
        await afp.write(orjson.dumps(ok_centers, default=orjson_default_handler))


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
    job = list(ALL_RUNNERS)
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

    all_script_information: list["Information"] = []
    all_async_script_runners = []
    for RunnerObj in scripts_to_run:
        this_runner = RunnerObj()
        all_script_information.append(this_runner.set_information())
        all_async_script_runners.append(RunnerObj().run(disk_cache, imgur, prefix))
    async with asyncio.Semaphore(10):
        await asyncio.gather(*all_async_script_runners, return_exceptions=True)
        await generate_location(all_script_information)

        await last_week_update.set_last_week_items()


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
    SENTRY_SDK_DNS = runtime_setting.SENTRY_SDK_DNS if not runtime_setting.IS_DEBUG else None
    sentry_sdk.init(dsn=SENTRY_SDK_DNS, traces_sample_rate=1.0)
    asyncio.run(main())
    # asyncio.run(main(args.worker, args.max_worker))
