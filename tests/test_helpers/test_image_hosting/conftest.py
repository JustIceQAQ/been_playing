import pytest
import uuid


@pytest.fixture(scope="function")
def public_id():
    return f"pytest-{uuid.uuid4().hex}"


@pytest.fixture(scope="package")
def cloudinary_creds():
    from configs.settings import get_settings

    settings = get_settings()
    return (settings.CLOUDINARY_CLOUD_NAME, settings.CLOUDINARY_API_KEY, settings.CLOUDINARY_API_SECRET)


@pytest.fixture(scope="package")
def initialized_cloudinary(cloudinary_creds):
    from helpers.image_hosting.cloudinary.helper import get_initialized_cloudinary_image_hosting

    return get_initialized_cloudinary_image_hosting(*cloudinary_creds)


@pytest.fixture(scope="package")
def image_but_not_exts() -> str:
    return "https://systemeblob.blob.core.windows.net/allticket-prod/media/b2ead3f0-79de-4dc5-9c5e-406be0ea259e.%E7%AF%80%E7%9B%AE%E5%9C%96(%E6%B4%BB%E5%8B%95%E4%B8%8A%E6%9E%B6%E5%9C%96%E6%AA%94)_1200x675"


@pytest.fixture(scope="package")
def huge_image() -> str:
    return "https://svs.gsfc.nasa.gov/vis/a030000/a030800/a030877/frames/5760x3240_16x9_01p/BlackMarble_2016_1400m_africa_m_labeled.png"
