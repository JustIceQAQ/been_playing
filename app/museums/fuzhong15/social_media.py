from helpers.storage.social_media import SocialMedia


class FuZhong15SocialMedia:
    @staticmethod
    def get_social_media() -> SocialMedia:
        return SocialMedia(
            facebook="https://www.facebook.com/FZfifteen",
            instagram="https://www.instagram.com/fzfifteen/?hl=zh-tw",
            youtube="https://www.youtube.com/channel/UCQ5HSHDNqxu4RyhDHN6jL4Q",
        )
