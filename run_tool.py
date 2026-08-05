import asyncio
import pathlib
from typing import TYPE_CHECKING

import aiofiles
import httpx2 as httpx

from app.script import ALL_RUNNERS

if TYPE_CHECKING:
    from helpers.storage.helper import Information

URL_ROOT = "https://raw.githubusercontent.com/JustIceQAQ/been_playing/auto/data-update/data/v2/{code_name}.json"

SAVA_FOLDER_PATH = pathlib.Path(__file__).parent.absolute() / "fixture/local_save"

ALL_URL = []


async def save_json_to_file(data: str, code_name: str):
    async with aiofiles.open(SAVA_FOLDER_PATH / f"{code_name}.json", "w") as f:
        await f.write(data)


async def get_url_json(client: httpx.AsyncClient, info: "Information"):
    code_name = info.code_name
    url = URL_ROOT.format(code_name=code_name)
    ALL_URL.append(url)
    response = await client.get(URL_ROOT.format(code_name=code_name))
    response.raise_for_status()
    await save_json_to_file(response.text, code_name)


async def main():
    jobs = list(ALL_RUNNERS)
    async with httpx.AsyncClient(timeout=None, follow_redirects=True) as client:
        tasks = [get_url_json(client, job().set_information()) for job in jobs]
        await asyncio.gather(*tasks)

    async with aiofiles.open(SAVA_FOLDER_PATH / "_ALL_URL.json", "w") as f:
        await f.write("\n".join(ALL_URL))


if __name__ == "__main__":
    asyncio.run(main())
