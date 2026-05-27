import asyncio

from typing import cast, TYPE_CHECKING
from app.museums.sshm.parse import SSHMParse
from app.museums.sshm.information import SSHMInformation
from app.museums.sshm.social_media import SSHMSocialMedia
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.utils_helper import month_3


from helpers.crawler.niquests.helper import NiquestsAsyncSession


from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation


if TYPE_CHECKING:
    from helpers.storage.helper import Information
    from helpers.storage.social_media import SocialMedia


class SSHMRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = SSHMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return SSHMInformation.get_information()

    def set_social_media(self) -> "SocialMedia":
        return SSHMSocialMedia.get_social_media()

    async def fetch_response(self):
        headers = generate_headers(host="www.sshm.ntpc.gov.tw")
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            main_response = await client.get(
                "https://www.sshm.ntpc.gov.tw/submenu?usein=2&psid=0G244574557570145140", cookies=cookies
            )
            main_parse = SelectolaxTranslation().translation_to_object(main_response.text)

            target_url = main_parse.css_first("a[title='當期展覽']").attributes.get("href")
            response = await client.get(target_url, cookies=cookies)
            response_parse = SelectolaxTranslation().translation_to_object(response.text)
            items = response_parse.css("table.ListTable tbody tr td.title a")
            responses = await asyncio.gather(
                *[
                    client.get("https://www.sshm.ntpc.gov.tw" + item.attributes.get("href"), cookies=cookies)
                    for item in items
                ]
            )
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        return parsed


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await SSHMRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
