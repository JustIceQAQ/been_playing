import json
from typing import Any

from helpers.translation.base import TranslationInit


class JsonTranslation(TranslationInit):
    def translation_to_object(self, text: dict[Any, Any] | None, *args, **kwargs) -> dict[Any, Any] | None:
        if text is None:
            return None
        return text


class DevalueToJsonTranslation(TranslationInit):
    REACTIVE = {"ShallowReactive", "Reactive", "Ref", "ShallowRef", "EmptyRef", "EmptyShallowRef"}
    SPECIAL = {-1: None, -2: None, -3: float("nan"), -4: float("inf"), -5: float("-inf"), -6: -0.0}

    def translation_to_object(self, text: str | list | None, *args, **kwargs) -> Any:
        if text is None:
            return None
        flat = json.loads(text) if isinstance(text, str) else text
        return self.unflatten(flat)

    def unflatten(self, flat: list) -> Any:
        cache: dict[int, Any] = {}

        def resolve(i: int) -> Any:
            if i in self.SPECIAL:
                return self.SPECIAL[i]
            if i in cache:
                return cache[i]
            v = flat[i]

            if isinstance(v, list):
                tag = v[0] if v and isinstance(v[0], str) else None
                if tag in self.REACTIVE:
                    cache[i] = None
                    cache[i] = resolve(v[1])
                elif tag == "Set":
                    cache[i] = [resolve(x) for x in v[1:]]
                elif tag == "Map":
                    cache[i] = {}
                    for k, val in zip(v[1::2], v[2::2], strict=True):
                        cache[i][resolve(k)] = resolve(val)
                elif tag in ("Date", "BigInt"):
                    cache[i] = v[1]  # 字面字串,不是索引
                elif tag == "null":
                    cache[i] = {}
                    for k, val in zip(v[1::2], v[2::2], strict=True):
                        cache[i][k] = resolve(val)
                else:
                    out: list = []
                    cache[i] = out
                    out.extend(resolve(x) for x in v)
            elif isinstance(v, dict):
                out = {}
                cache[i] = out
                for k, x in v.items():
                    out[k] = resolve(x)
            else:
                cache[i] = v
            return cache[i]

        return resolve(0)
