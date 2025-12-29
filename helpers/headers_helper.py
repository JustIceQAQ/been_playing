import secrets

from fake_useragent import UserAgent

UA = UserAgent(browsers="chrome", os=["windows", "macos"], platforms="pc")


def get_header() -> dict[str, str]:
    return {
        "user-agent": UA.random,
    }


def get_cookies(
    need_phpsessid: bool | None = False,
    need_asp_net_session_id: bool = False,
    need_js_ession_id: bool = False,
    need_consent: bool | None = False,
) -> dict[str, str]:
    this_data = {}
    if need_phpsessid:
        this_data["PHPSESSID"] = secrets.token_hex(16)

    if need_asp_net_session_id:
        this_data["ASP.NET_SessionId"] = secrets.token_hex(16)

    if need_js_ession_id:
        this_data["JSESSIONID"] = secrets.token_hex(16)

    if need_consent:
        this_data["CONSENT"] = "YES+"

    if this_data:
        return this_data
