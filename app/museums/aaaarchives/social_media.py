from helpers.storage.social_media import SocialMedia


class AAAArchivesSocialMedia:
    @staticmethod
    def get_social_media() -> SocialMedia:
        return SocialMedia(
            facebook="https://www.facebook.com/Archives.ing/",
            instagram="https://www.instagram.com/na.afe/",
            youtube="https://www.youtube.com/user/taiwanarchives",
        )
