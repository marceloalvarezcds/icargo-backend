from fastapi import UploadFile  # type: ignore
from requests import post

from app.config import PICTSHARE_API, PictShareSettings
from app.schemas.pictshare_response import PictShareResponse

settings = PictShareSettings()


async def upload_image(file: UploadFile) -> PictShareResponse:
    url = f"{settings.PICTSHARE_DOCKER}/{settings.PICTSHARE_UPLOAD}"
    data = await file.read()
    files = {"file": (file.filename, data, file.content_type)}
    response = post(url, files=files)
    return PictShareResponse.parse_obj(response.json())


async def upload_and_get_image_url(file: UploadFile) -> str:
    response = await upload_image(file)
    return f"{PICTSHARE_API}/{response.hash}"
