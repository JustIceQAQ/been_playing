import base64
import json

from pydantic import BaseModel
from urllib.parse import quote


class CommonConfig(BaseModel):
    brand: str = "wix"
    host: str = "VIEWER"
    BSI: str
    siteRevision: str = "3128"
    renderingFlow: str = "NONE"
    language: str = "zh"
    locale: str = "zh-tw"

    def to_query(self) -> str:
        json_str = self.model_dump_json()
        return quote(json_str)


def query_p(app_id: str) -> str:
    return base64.b64encode(
        json.dumps(
            {
                "dataCollectionId": "Exhibitionsnew",
                "query": {
                    "filter": {},
                    "sort": [{"fieldName": "sortId", "order": "DESC"}],
                    "paging": {"offset": 0, "limit": 10},
                    "fields": [],
                },
                "referencedItemOptions": [],
                "returnTotalCount": True,
                "environment": "LIVE",
                "appId": app_id,
            }
        ).encode("utf-8")
    ).decode("utf-8")
