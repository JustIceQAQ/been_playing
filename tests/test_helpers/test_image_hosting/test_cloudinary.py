import pytest

from helpers.crawler.wreq.helper import WReqAsyncClient
from helpers.image_hosting.cloudinary.helper import get_initialized_cloudinary_image_hosting
from helpers.proxy_helper import _get_proxy


def test_import_class():
    from helpers.image_hosting.cloudinary import CloudinaryImageHosting  # noqa


@pytest.mark.parametrize(
    "args",
    [
        (),
        (None,),
        (None, None),
    ],
)
def test_cloudinary_init_missing_args_parametrized(args):
    with pytest.raises(TypeError):
        get_initialized_cloudinary_image_hosting(*args)


@pytest.mark.parametrize(
    "c_name, a_key, a_secret",
    [
        (None, None, None),
        ("cloud_name", None, None),
        (None, "api_key", None),
        (None, None, "api_secret"),
        ("cloud_name", "api_key", None),
        (None, "api_key", "api_secret"),
        ("cloud_name", None, "api_secret"),
    ],
)
def test_get_initialized_cloudinary_image_hosting_invalid_args(c_name, a_key, a_secret):
    with pytest.raises(ValueError):
        get_initialized_cloudinary_image_hosting(c_name, a_key, a_secret)


def test_get_initialized_cloudinary_image_hosting_func_retrun_type(cloudinary_creds):
    from helpers.image_hosting.cloudinary import CloudinaryImageHosting

    assert isinstance(get_initialized_cloudinary_image_hosting(*cloudinary_creds), CloudinaryImageHosting)


def test_init(cloudinary_creds):
    c1 = get_initialized_cloudinary_image_hosting(*cloudinary_creds)
    c2 = get_initialized_cloudinary_image_hosting(*cloudinary_creds)
    assert id(c1) == id(c2)


@pytest.mark.asyncio
async def test_upload_from_url(initialized_cloudinary, image_but_not_exts, public_id):
    image_url = image_but_not_exts
    await initialized_cloudinary.upload_from_url(
        image_url,
        public_id=public_id,
    )
    await initialized_cloudinary.destroy_from_public_id(public_id)


@pytest.mark.asyncio
async def test_upload_from_file(initialized_cloudinary, image_but_not_exts, public_id):
    proxies = _get_proxy()
    image_url = image_but_not_exts
    async with WReqAsyncClient(proxies=proxies.to_wreq()) as client:
        response = await client.get(image_url)
        if not response.status.is_success():
            return None
        image_bytes = await response.bytes()

    await initialized_cloudinary.upload_from_file(
        image_bytes,
        public_id=public_id,
    )
    await initialized_cloudinary.destroy_from_public_id(public_id)


@pytest.mark.asyncio
async def test_upload_from_huge_file(initialized_cloudinary, huge_image, public_id):
    proxies = _get_proxy()
    image_url = huge_image

    await initialized_cloudinary.upload(
        image_url,
        proxies,
        public_id=public_id,
    )
    await initialized_cloudinary.destroy_from_public_id(public_id)
