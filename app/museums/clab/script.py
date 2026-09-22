import asyncio
import json
import re
from typing import cast

import bs4

from app.museums.clab.parse import CLabParse
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.wreq import WReqAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


def has_event_type(event: dict, target_slug: str) -> bool:
    nodes = event.get("eventTypes", {}).get("nodes", [])
    return any(node.get("slug") == target_slug for node in nodes)


class CLabRunner(RunnerInit):
    """臺灣當代文化實驗場 C-LAB"""

    translation = BeautifulSoupTranslation
    use_parse = CLabParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.daan_63000030,
            fullname="台灣當代文化實驗場 C-Lab",
            code_name="CLab",
            external_link="https://clab.org.tw/zh/events?__rw=1",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.039263447268308, 121.53884705257425"),
                raw_coordinates="25.039263447268308, 121.53884705257425",
            ),
            venue_type=VenueType.ART_VILLAGE,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(other_cookies={"language": "zh"})

        async with WReqAsyncClient(headers=headers, cookies=cookies) as client:
            responses = await client.get("https://clab.org.tw/zh/events?__rw=1")
        return await responses.text()

    def extract_json_array(self, text: str, key_name: str) -> list[dict] | None:
        """
        從 Next.js RSC 的 self.__next_f.push([...]) 原始內容中，
        安全擷取指定 key 對應的 JSON 陣列。
        """
        # 1) push() 的參數本身是合法 JSON 字串，先解跳脫還原成明碼文字
        decoded_chunks = []
        for m in re.finditer(r'self\.__next_f\.push\(\[\s*\d+\s*,\s*(".*?")\s*\]\)', text, re.S):
            literal = m.group(1)
            try:
                decoded_chunks.append(json.loads(literal))
            except json.JSONDecodeError:
                decoded_chunks.append(literal[1:-1].replace('\\"', '"').replace("\\\\", "\\").replace("\\n", "\n"))
        decoded_text = "\n".join(decoded_chunks) if decoded_chunks else text

        key_pattern = f'"{key_name}"'
        key_pos = decoded_text.find(key_pattern)
        if key_pos == -1:
            return None
        colon_pos = decoded_text.find(":", key_pos + len(key_pattern))
        if colon_pos == -1:
            return None
        start = decoded_text.find("[", colon_pos)
        if start == -1:
            return None

        depth = 0
        in_string = False
        escape = False
        end = None
        for i in range(start, len(decoded_text)):
            ch = decoded_text[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
            else:
                if ch == '"':
                    in_string = True
                elif ch == "[":
                    depth += 1
                elif ch == "]":
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
        if end is None:
            return None

        raw_array = decoded_text[start : end + 1]
        return json.loads(raw_array)

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        target_script = None
        key_name = "initialEvents"
        for script in parsed.find_all("script"):
            if script.string and (key_name in script.string):
                target_script = script.string
                break
        if not target_script:
            return []
        events = self.extract_json_array(target_script, key_name)
        if events is None:
            return []
        exhibitions = [e for e in events if has_event_type(e, "exhibition")]
        return exhibitions[:10]


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await CLabRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
