from functools import lru_cache

from configs.settings import get_settings
from helpers.image_hosting.cloudinary import CloudinaryImageHosting


@lru_cache
def get_initialized_cloudinary_image_hosting_depends() -> CloudinaryImageHosting:
    runtime_setting = get_settings()
    return CloudinaryImageHosting(
        runtime_setting.CLOUDINARY_CLOUD_NAME,
        runtime_setting.CLOUDINARY_API_KEY,
        runtime_setting.CLOUDINARY_API_SECRET,
    )
