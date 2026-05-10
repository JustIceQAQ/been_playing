import asyncio

import cloudinary
import cloudinary.uploader


class CloudinaryImageHost:
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        self.cloudinary = cloudinary
        self.cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,  # Click 'View API Keys' above to copy your API secret
            secure=True,
        )

    async def upload(self, image_url: str) -> str | None:
        loop = asyncio.get_running_loop()
        try:
            upload_result = await loop.run_in_executor(None, lambda: self.cloudinary.uploader.upload(image_url))
            return upload_result.get("secure_url")
        except Exception as e:
            print(f"Cloudinary Error: {e}")
            return None


async def main():
    ci = CloudinaryImageHost("", "", "")
    result = await ci.upload("")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
