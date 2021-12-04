import os

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoCamion
from app.services import upload_and_get_binary_url

dir_path = os.path.dirname(os.path.realpath(__file__))
IMAGES = os.path.join(dir_path, "tipo_camion_images")


def tipo_camion_seeds(db: Session):
    try:
        with open(f"{IMAGES}/desplazado.png", "rb") as image:
            image_url = upload_and_get_binary_url(image)
            db.add(TipoCamion(descripcion="Trucky", tipo_imagen=image_url))
        with open(f"{IMAGES}/triple_eje.png", "rb") as image:
            image_url = upload_and_get_binary_url(image)
            db.add(TipoCamion(descripcion="Chasis & Acoplado", tipo_imagen=image_url))
        db.add(TipoCamion(descripcion="1S.2D (trucado)", tipo_imagen=None))
        db.add(TipoCamion(descripcion="1S.1S (sencillo)", tipo_imagen=None))
        db.add(TipoCamion(descripcion="1S.1D (normal)", tipo_imagen=None))
        db.commit()
    except IntegrityError:
        db.rollback()
