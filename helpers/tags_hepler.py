from enum import Enum


class ActionEnum(str, Enum):
    Exhibition = "展覽"
    Lecture = "講座"
    Workshop = "工作坊"
    Outside = "館外活動"
    Activity = "活動"
    Limited = "期間限定"
    Other = "其他"


ACTION_TAG_FAMILIES: dict[ActionEnum, set[str]] = {
    ActionEnum.Exhibition: {"展覽", "Exhibition", "exhibition", "展演活動"},
    ActionEnum.Lecture: {"講座", "Lecture", "演講", "論壇講座", ""},
    ActionEnum.Workshop: {"工作坊", "Workshop"},
    ActionEnum.Outside: {"館外活動", "Outside", "outdoor"},
    ActionEnum.Activity: {"活動", "Activity", "Event", "市集活動", "品牌活動", ""},
    ActionEnum.Limited: {"期間限定", "期間", "限定", "期間展", "期間限定店"},
    ActionEnum.Other: {"其他", "Other"},
}


def normalize_tag(tag: str) -> ActionEnum | str | None:
    normalized = tag.strip()
    for action, synonyms in ACTION_TAG_FAMILIES.items():
        if normalized in synonyms:
            return action.value
    return normalized
