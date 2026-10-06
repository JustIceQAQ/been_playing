def find_exhibition_list(data: dict) -> list:
    for key, value in data["data"].items():
        if key.startswith("exhibition-list-") and isinstance(value, dict) and "contentList" in value:
            return value["contentList"]
    return []


def get_event_category_data(data: dict) -> dict:
    event_categories = data["state"]["$sglobalCategories"]["event_category:events:zh-TW"]

    return {
        event_category["id"]: event_category["name"].strip().replace("\t", " ") for event_category in event_categories
    }


def get_event_venue_data(data: dict) -> dict:
    event_venues = data["state"]["$sglobalCategories"]["event_venue:events:zh-TW"]
    return {event_venue["id"]: event_venue["name"].strip().replace("\t", " ") for event_venue in event_venues}
