from typing import Dict

from helper.parse_helper import ParseInit


class TFAMParse(ParseInit):
    def __init__(self, item: Dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return str(self.item.get("ExName", "-"))

    def get_date(self, *args, **kwargs) -> str:
        begin_date = self.item.get("BeginDate", None)
        end_date = self.item.get("EndDate", None)
        return f"{begin_date} ~ {end_date}".replace("/", "-")

    def get_address(self, *args, **kwargs) -> str:
        return self.item.get("Area", "-")

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        now_play_img = self.item.get("NowPlayImg", None)

        return "{}/File/{}".format(target_domain, now_play_img.replace("\\", "/"))

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")

        return "{}/Exhibition/Exhibition_page.aspx?id={}".format(
            target_domain, self.item.get("ExID", "-")
        )
