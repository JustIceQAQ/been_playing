import asyncio
import inspect
from json import JSONDecodeError

import sentry_sdk
from wreq import DecodingError


async def safe_json(response, code: str, max_chars: int = 2000) -> dict:
    try:
        get_json_result = response.json()
        if inspect.iscoroutine(get_json_result) or asyncio.iscoroutine(get_json_result):
            get_json_result = await get_json_result
        return get_json_result
    except (JSONDecodeError, DecodingError) as e:
        with sentry_sdk.new_scope() as scope:
            scope.set_context(
                "HTTP Response Details",
                {
                    "code": code,
                    "status_code": response.status_code,
                    "response_text": response.text[:max_chars],
                    "url": str(response.url),
                    "headers": dict(response.headers),
                },
            )
            sentry_sdk.capture_exception(e)
        return {}
