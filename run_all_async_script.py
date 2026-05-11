import argparse
import asyncio
import orjson
import logging
from pathlib import Path
import aiofiles
import sentry_sdk
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from app.script import ALL_RUNNERS
from configs.settings import get_settings
from helpers.cache import DiskCache, NoneCache
from helpers.storage.helper import (
    Information,
    Coordinate,
    orjson_default_handler,
    last_week_update,
    execution_stats,
)
from helpers.crawler.scraper.helper import available_scraper_async_client
from helpers.image_hosting.none.helper import NoneImageHosting
from helpers.image_hosting.cloudinary.helper import CloudinaryImageHosting

ROOT_PATH = Path(__file__).parent.absolute()


async def generate_venue_meta(information: list["Information"]):
    venues = []
    for info in information:
        city_name = None
        area_name = None
        if info.location_code is not None:
            city_name = info.location_code.city.name
            area_name = info.location_code.area.name if info.location_code.area else None
        venues.append(
            {
                "code_name": info.code_name,
                "fullname": info.fullname,
                "venue_type": info.venue_type,
                "city": city_name,
                "area": area_name,
            }
        )

    async with aiofiles.open(ROOT_PATH / "data" / "v2" / "_VENUE_META.json", "wb+") as afp:
        await afp.write(orjson.dumps(venues, default=orjson_default_handler))


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
    sem = asyncio.Semaphore(10)
    runtime_setting = get_settings()

    # logging init
    logging.basicConfig(
        level=logging.DEBUG if runtime_setting.IS_DEBUG else logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )
    image_host = NoneImageHosting()
    if (not runtime_setting.IS_DEBUG) and (runtime_setting.is_cloudinary_available):
        assert runtime_setting.CLOUDINARY_CLOUD_NAME is not None
        assert runtime_setting.CLOUDINARY_API_KEY is not None
        assert runtime_setting.CLOUDINARY_API_SECRET is not None
        image_host = CloudinaryImageHosting(
            runtime_setting.CLOUDINARY_CLOUD_NAME,
            runtime_setting.CLOUDINARY_API_KEY,
            runtime_setting.CLOUDINARY_API_SECRET,
        )

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
    named_runners: list[tuple[str, object]] = []
    for RunnerObj in scripts_to_run:
        this_runner = RunnerObj()
        all_script_information.append(this_runner.set_information())
        named_runners.append((RunnerObj.__name__, RunnerObj().run(disk_cache, image_host, prefix)))

    total = len(named_runners)
    done_count = 0
    is_debug = runtime_setting.IS_DEBUG
    console = Console()
    failed: list[str] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        TimeElapsedColumn(),
        BarColumn(),
        MofNCompleteColumn(),
        console=console,
        disable=not is_debug,
    ) as progress:
        overall = progress.add_task("[bold cyan]總進度", total=total)

        async def tracked_run(name: str, coro):
            nonlocal done_count
            async with sem:
                task_id = progress.add_task(f"[yellow]{name}", total=None)
                try:
                    result = await coro
                    done_count += 1
                    progress.update(overall, advance=1)
                    if is_debug:
                        console.log(f"[green]OK [/green] {name}")
                    return result
                except Exception as e:
                    done_count += 1
                    failed.append(name)
                    progress.update(overall, advance=1)
                    cause = e.__cause__ or e
                    if is_debug:
                        console.log(f"[red]ERR[/red] {name} — {type(cause).__name__}: {cause}")
                    return e
                finally:
                    progress.remove_task(task_id)

        await asyncio.gather(*[tracked_run(name, coro) for name, coro in named_runners])

    if failed and is_debug:
        console.print(f"\n[bold red]失敗 ({len(failed)}):[/bold red] {', '.join(failed)}")
    await generate_location(all_script_information)
    await generate_venue_meta(all_script_information)

    await last_week_update.set_last_week_items()
    await execution_stats.save()


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
