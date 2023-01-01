import asyncio
import logging
import os
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv

from exhibition.cksmh.async_script import CKSMHRunnerAsync
from exhibition.jam_async_script import JamRunnerAsync
from helper.image_helper import ImgurImage
from helper.notify_helper import LogNotify  # LineNotify , NoneNotify


async def main():
    # check env values
    IS_DEBUG = os.getenv("IS_DEBUG", False)
    CLIENT_ID = os.getenv("IMGUR_API_CLIENT_ID", False)
    CLIENT_SECRET = os.getenv("IMGUR_API_CLIENT_SECRET", False)
    USE_PICKLED = os.getenv("USE_PICKLED", True)
    # LINE_NOTIFY_API = os.getenv("LINE_NOTIFY_API", False)

    # logging init
    logging.basicConfig(
        level=logging.DEBUG if IS_DEBUG else logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )
    runtime_logging = logging.getLogger("runtime_logging")

    # Imgur image
    file_path = ROOT_DIR / "data" / "cache_file.json"
    imgur_image = ImgurImage()
    imgur_image.load_cache_file(file_path)

    # local notify (use logging)
    log_notify = LogNotify(runtime_logging)

    # if runtime process except
    # if IS_DEBUG is False and LINE_NOTIFY_API:
    #     runtime_notify = LineNotify(LINE_NOTIFY_API)
    # else:
    #     runtime_notify = NoneNotify()

    if CLIENT_ID and CLIENT_SECRET:
        imgur_image.login(CLIENT_ID, CLIENT_SECRET)
        log_notify.send_message("imgur api is login", log_notify.LogLevel.INFO)

    all_async_script_runners = [
        CKSMHRunnerAsync().run(use_pickled=USE_PICKLED),
        JamRunnerAsync().run(use_pickled=USE_PICKLED),
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
