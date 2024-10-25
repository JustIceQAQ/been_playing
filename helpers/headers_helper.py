from fake_useragent import UserAgent

UA = UserAgent(browsers="chrome", os=["windows", "macos"], platforms="pc")


def get_header() -> dict[str, str]:
    return {
        "User-Agent": UA.random,
    }
