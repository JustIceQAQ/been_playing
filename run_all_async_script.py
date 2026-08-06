import argparse
import asyncio
import logging
from datetime import UTC, datetime
from pathlib import Path

import aiofiles
import orjson
import sentry_sdk
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from app.script import ALL_RUNNERS
from configs.settings import get_settings
from helpers.cache import disk_cache, none_cache
from helpers.image_hosting import get_initialized_cloudinary_image_hosting, none_image_hosting
from helpers.storage.coordinate import Coordinate
from helpers.storage.helper import (
    Information,
    execution_stats,
    last_week_update,
    orjson_default_handler,
)
from helpers.symbol.venue import VenueType

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
                    if info.branch_coordinates.location_code.area is not None
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
                area_name = (
                    this_coordinate.location_code.area.name if this_coordinate.location_code.area is not None else None
                )
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
        "last_update": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
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
        level=logging.WARNING if runtime_setting.IS_DEBUG else logging.ERROR,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )
    use_image_host = none_image_hosting
    if (not runtime_setting.IS_DEBUG) and (runtime_setting.is_cloudinary_available):
        use_image_host = get_initialized_cloudinary_image_hosting(
            runtime_setting.CLOUDINARY_CLOUD_NAME,
            runtime_setting.CLOUDINARY_API_KEY,
            runtime_setting.CLOUDINARY_API_SECRET,
        )

    use_cache = none_cache if runtime_setting.IS_DEBUG else disk_cache
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

    all_script_information: list[Information] = []
    runner_items: list[tuple[type, Information]] = []
    for RunnerObj in scripts_to_run:
        runner_instance = RunnerObj()
        info = runner_instance.set_information()
        all_script_information.append(info)
        runner_items.append((RunnerObj, info))

    total = len(runner_items)
    is_debug = runtime_setting.IS_DEBUG
    console = Console()
    failed: list[str] = []

    concurrency_limit = 4
    sem = asyncio.Semaphore(concurrency_limit)

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

        async def run_single_runner(RunnerObj: type, info: Information):
            async with sem:
                name = RunnerObj.__name__
                task_id = progress.add_task(f"[yellow]{name}", total=None)
                start_time = asyncio.get_event_loop().time()
                try:
                    # 延後到此處才實例化並執行 run()
                    runner_instance = RunnerObj()
                    await runner_instance.run(use_cache, use_image_host, prefix, image_sem)

                    elapsed = asyncio.get_event_loop().time() - start_time
                    execution_stats.record(
                        code_name=info.code_name,
                        fullname=info.fullname,
                        execution_time=elapsed,
                        last_update=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    )
                    if is_debug:
                        console.log(f"[green]OK [/green] {name}")
                except Exception as e:
                    failed.append(name)
                    cause = e.__cause__ or e
                    # 避免 console 或 sentry 拋出二次例外導致外層潰散
                    try:
                        console.print(f"[red]ERR[/red] {name} — {type(cause).__name__}: {cause}")
                        sentry_sdk.capture_exception(e)
                    except Exception as inner_e:
                        logging.error(f"Error handling failure for {name}: {inner_e}")
                except BaseException as e:
                    # 攔截 CancelledError / SystemExit 以外的嚴重例外
                    if isinstance(e, (asyncio.CancelledError, KeyboardInterrupt)):
                        raise
                    failed.append(name)
                    console.print(f"[red]CRITICAL ERR[/red] {name} — {type(e).__name__}: {e}")
                finally:
                    progress.update(overall, advance=1)
                    progress.remove_task(task_id)

        tasks = [run_single_runner(RunnerObj, info) for RunnerObj, info in runner_items]
        await asyncio.gather(*tasks, return_exceptions=True)

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
