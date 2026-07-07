from helpers.storage.social_media import SocialMedia


class NTPCSocialMedia:
    @staticmethod
    def get_social_media() -> SocialMedia:
        return SocialMedia(
            instagram="https://www.instagram.com/yinggeceramicsmuseum/?hl=zh-tw",
            facebook="https://www.facebook.com/YCMuseum/?locale=zh_TW",
            x="https://x.com/yinggeceramics1",
        )
