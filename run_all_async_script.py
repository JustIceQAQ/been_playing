import argparse
import asyncio
import orjson
import logging
from datetime import datetime, timezone
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
    orjson_default_handler,
    last_week_update,
    execution_stats,
)
from helpers.storage.coordinate import Coordinate
from helpers.symbol.venue import VenueType
from helpers.crawler.scraper.helper import available_scraper_async_client
from helpers.image_hosting.none.helper import NoneImageHosting
from helpers.image_hosting.cloudinary.helper import CloudinaryImageHosting

ROOT_PATH = Path(__file__).parent.absolute()


async def generate_venue_meta(information: list["Information"]):
    venues = []
    for info in information:
        city_name = None
        area_name = None
        if isinstance(info.branch_coordinates, Coordinate):
            if info.branch_coordinates.location_code is not None:
                city_name = info.branch_coordinates.location_code.city.name
                area_name = (
                    info.branch_coordinates.location_code.area.name
                    if info.branch_coordinates.location_code.area.name
                    else None
                )
            else:
                if info.location_code is not None:
                    city_name = info.location_code.city.name
                    area_name = info.location_code.area.name if info.location_code.area else None

        elif isinstance(info.branch_coordinates, list):
            this_coordinate = info.branch_coordinates[0]
            if this_coordinate.location_code is not None:
                city_name = this_coordinate.location_code.city.name
                area_name = this_coordinate.location_code.area.name if this_coordinate.location_code.area.name else None
        elif info.location_code is not None:
            city_name = info.location_code.city.name
            area_name = info.location_code.area.name if info.location_code.area else None

        if isinstance(info.branch_coordinates, list):
            use_info = info.branch_coordinates[0]
        else:
            use_info = info.branch_coordinates

        result = {
            "code_name": info.code_name,
            "fullname": info.fullname,
            "venue_type": info.venue_type,
            "city": city_name,
            "area": area_name,
        }

        if info.venue_type == VenueType.PLATFORM:
            venues.append(result)
            continue

        has_location_code = (use_info.location_code is not None) if use_info else False
        has_address = (use_info.address is not None) if use_info else False
        has_geo_point = (use_info.geo_point is not None) if use_info else False
        has_open_street_map = (use_info.open_street_map is not None) if use_info else False
        has_wiki = (use_info.wiki is not None) if use_info else False
        has_google_maps = (use_info.google_maps is not None) if use_info else False

        has_flags = [
            has_location_code,
            has_address,
            has_geo_point,
            has_open_street_map,
            has_wiki,
            has_google_maps,
        ]

        if not all(has_flags):
            check_coordinate = {
                "has_location_code": has_location_code,
                "has_address": has_address,
                "has_geo_point": has_geo_point,
                "has_open_street_map": has_open_street_map,
                "has_wiki": has_wiki,
                "has_google_maps": has_google_maps,
            }
            failed = {k: v for k, v in check_coordinate.items() if not v}
            if failed:
                result["check_coordinate"] = failed

        venues.append(result)

    payload = {
        "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "venues": venues,
    }
    async with aiofiles.open(ROOT_PATH / "data" / "v2" / "_VENUE_META.json", "wb+") as afp:
        await afp.write(orjson.dumps(payload, default=orjson_default_handler))


async def generate_location(information: list["Information"]):
    console = Console()
    ok_centers = []

    for location in information:
        fullname = location.fullname
        if isinstance(location.branch_coordinates, Coordinate):
            if location.branch_coordinates.geo_point is not None:
                latitude = location.branch_coordinates.geo_point.latitude
                longitude = location.branch_coordinates.geo_point.longitude
            else:
                console.log(f"{location.code_name} not use geo_point")
                latitude = location.branch_coordinates.latitude
                longitude = location.branch_coordinates.longitude

            ok_centers.append(
                {
                    "fullname": fullname,
                    "latitude": latitude,
                    "longitude": longitude,
                    "venue_type": location.venue_type,
                    "external_link": location.external_link,
                }
            )
            continue
        if isinstance(location.branch_coordinates, list):
            for branch_coordinate in location.branch_coordinates:
                name = "None" if (this_name := branch_coordinate.name) is None else this_name
                if branch_coordinate.geo_point is not None:
                    latitude = branch_coordinate.geo_point.latitude
                    longitude = branch_coordinate.geo_point.longitude
                else:
                    console.log(f"{location.code_name} not use geo_point")
                    latitude = branch_coordinate.latitude
                    longitude = branch_coordinate.longitude
                ok_centers.append(
                    {
                        "fullname": fullname + "-" + name,
                        "latitude": latitude,
                        "longitude": longitude,
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
    image_sem = asyncio.Semaphore(5)
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
        named_runners.append((RunnerObj.__name__, RunnerObj().run(disk_cache, image_host, prefix, image_sem)))

    total = len(named_runners)
    is_debug = runtime_setting.IS_DEBUG
    console = Console()
    failed: list[str] = []

    task_queue = asyncio.Queue()
    for item in named_runners:
        await task_queue.put(item)

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

        async def worker_loop():
            while not task_queue.empty():
                try:
                    name, coro = await task_queue.get()
                except asyncio.QueueEmpty:
                    break

                task_id = progress.add_task(f"[yellow]{name}", total=None)
                try:
                    await coro
                    progress.update(overall, advance=1)
                    if is_debug:
                        console.log(f"[green]OK [/green] {name}")
                except Exception as e:
                    failed.append(name)
                    progress.update(overall, advance=1)
                    cause = e.__cause__ or e
                    # 關鍵：不論是否為 debug 模式，CI 環境失敗了就一定要印出錯誤
                    console.print(f"[red]ERR[/red] {name} — {type(cause).__name__}: {cause}")
                    sentry_sdk.capture_exception(e)
                finally:
                    progress.remove_task(task_id)
                    task_queue.task_done()

        concurrency_limit = 4
        workers = [asyncio.create_task(worker_loop()) for _ in range(concurrency_limit)]

        await task_queue.join()
        for w in workers:
            w.cancel()

    await generate_location(all_script_information)
    await generate_venue_meta(all_script_information)
    await last_week_update.set_last_week_items()
    await execution_stats.save()
    if failed:
        console.print(f"\n[bold red]失敗 ({len(failed)}):[/bold red] {', '.join(failed)}")


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
