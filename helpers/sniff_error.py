from json import JSONDecodeError

import sentry_sdk


def safe_json(response, code: str, max_chars: int = 2000) -> dict:
    try:
        return response.json()
    except JSONDecodeError as e:
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
        raise
