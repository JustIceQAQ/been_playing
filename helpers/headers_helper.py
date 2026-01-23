import secrets

from fake_useragent import UserAgent

UA = UserAgent(browsers="chrome", os=["windows", "macos"], platforms="pc")


def generate_headers(
    host: str | None = None,
    referer: str | None = None,
    origin: str | None = None,
    x_requested_with: str | None = None,
    need_upgrade_insecure_requests: bool | None = False,
    other_headers: dict | None = None,
    not_use_user_agent: bool = False,
) -> dict[str, str]:
    this_header = {
        "user-agent": UA.random,
        "dnt": "1",
    }
    if not_use_user_agent:
        this_header.pop("user-agent")

    if host:
        this_header["host"] = host
    if referer:
        this_header["referer"] = referer
    if origin:
        this_header["origin"] = origin

    if x_requested_with:
        this_header["x-requested-with"] = x_requested_with

    if need_upgrade_insecure_requests:
        this_header["upgrade-insecure-requests"] = "1"

    if other_headers:
        this_header |= other_headers

    return this_header


def generate_cookies(
    need_phpsessid: bool | None = False,
    need_asp_net_session_id: bool = False,
    need_js_ession_id: bool = False,
    need_consent: bool | None = False,
    need_laravel_session: bool | None = False,
    other_cookies: dict | None = None,
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

    if need_laravel_session:
        this_data["laravel_session"] = secrets.token_hex(20)

    if other_cookies:
        this_data |= other_cookies

    if this_data:
        return this_data
