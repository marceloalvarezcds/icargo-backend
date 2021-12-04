from typing import BinaryIO, Optional, Tuple, Union

from fastapi import HTTPException, UploadFile
from requests import post

from app.config import PICTSHARE_API, PictShareSettings
from app.schemas.pictshare_response import PictShareResponse

settings = PictShareSettings()

URL = f"{settings.PICTSHARE_DOCKER}/{settings.PICTSHARE_UPLOAD}"


def save_file(
    filename: str, data: Union[bytes, str], content_type: Optional[str] = "image/*"
) -> PictShareResponse:
    files = {"file": (filename, data, content_type)}
    response = post(URL, files=files)
    return PictShareResponse.parse_obj(response.json())


def upload_binary(file: BinaryIO) -> PictShareResponse:
    return save_file(file.name, file.read())


def upload_and_get_binary_url(file: BinaryIO) -> str:
    response = upload_binary(file)
    return f"{PICTSHARE_API}/{response.hash}"


async def upload_image(file: UploadFile) -> PictShareResponse:
    data = await file.read()
    return save_file(file.filename, data, file.content_type)


async def upload_and_get_image_url(file: UploadFile) -> str:
    response = await upload_image(file)
    return f"{PICTSHARE_API}/{response.hash}"


async def check_duplicate_images(
    image1: Optional[UploadFile], image2: Optional[UploadFile], err: str
) -> Tuple[Optional[str], Optional[str]]:
    url1 = await upload_and_get_image_url(image1) if image1 else None
    url2 = await upload_and_get_image_url(image2) if image2 else None
    if url1 and url2 and url1 == url2:
        raise HTTPException(status_code=400, detail=err)
    return (url1, url2)
