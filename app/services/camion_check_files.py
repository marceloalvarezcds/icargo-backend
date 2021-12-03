from typing import Optional, Tuple

from fastapi import UploadFile

from .pictshare import check_duplicate_images, upload_and_get_image_url


async def check_files(
    foto_file: Optional[UploadFile],
    foto_habilitacion_municipal_frente_file: Optional[UploadFile],
    foto_habilitacion_municipal_reverso_file: Optional[UploadFile],
    foto_habilitacion_transporte_frente_file: Optional[UploadFile],
    foto_habilitacion_transporte_reverso_file: Optional[UploadFile],
    foto_habilitacion_automotor_frente_file: Optional[UploadFile],
    foto_habilitacion_automotor_reverso_file: Optional[UploadFile],
) -> Tuple[
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
]:
    foto_url = await upload_and_get_image_url(foto_file) if foto_file else None
    (
        foto_habilitacion_municipal_frente_url,
        foto_habilitacion_municipal_reverso_url,
    ) = await check_duplicate_images(
        foto_habilitacion_municipal_frente_file,
        foto_habilitacion_municipal_reverso_file,
        "El reverso y el frente de la habilitación no pueden ser las mismas imágenes",
    )
    (
        foto_habilitacion_transporte_frente_url,
        foto_habilitacion_transporte_reverso_url,
    ) = await check_duplicate_images(
        foto_habilitacion_transporte_frente_file,
        foto_habilitacion_transporte_reverso_file,
        "El reverso y el frente del registro no pueden ser las mismas imágenes",
    )
    (
        foto_habilitacion_automotor_frente_url,
        foto_habilitacion_automotor_reverso_url,
    ) = await check_duplicate_images(
        foto_habilitacion_automotor_frente_file,
        foto_habilitacion_automotor_reverso_file,
        "El reverso y el frente del registro no pueden ser las mismas imágenes",
    )
    return (
        foto_url,
        foto_habilitacion_municipal_frente_url,
        foto_habilitacion_municipal_reverso_url,
        foto_habilitacion_transporte_frente_url,
        foto_habilitacion_transporte_reverso_url,
        foto_habilitacion_automotor_frente_url,
        foto_habilitacion_automotor_reverso_url,
    )
