from random import randrange
from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app import schemas
from app.models import TransactionalUser
from app.schemas import ApiResponseData
from app.services import generic_service as service
from app.utils import get_password_hash as get_pin_hash
from app.utils import verify_password as verify_pin

from .sms import send_sms


def create_transactional_user_with_pin(
    db: Session,
    data: schemas.TransactionalUserCreateForm,
    current_user: schemas.AuthPuntoVentaUser,
) -> ApiResponseData[schemas.TransactionalUser]:
    data.punto_venta_id = current_user.punto_venta_id
    transactional_user: TransactionalUser = service.create(
        TransactionalUser,
        db,
        data,  # type: ignore
        current_user.username,
        "El usuario transaccional",
        punto_venta_id=data.punto_venta_id,
        numero_documento=data.numero_documento,
    )
    pin = generate_pin(db, current_user.punto_venta_id)
    transactional_user.pin = get_pin_hash(pin)
    db.commit()
    send_pin_by_sms(transactional_user.telefono, pin)
    return ApiResponseData(data=schemas.TransactionalUser.from_orm(transactional_user))


def update_pin_by_id(
    db: Session, id: int, punto_venta_id: int
) -> ApiResponseData[schemas.TransactionalUser]:
    pin = generate_pin(db, punto_venta_id)
    transactional_user: TransactionalUser = service.get_by_id(TransactionalUser, db, id)
    transactional_user.pin = get_pin_hash(pin)
    db.commit()
    send_pin_by_sms(transactional_user.telefono, pin)
    return ApiResponseData(data=schemas.TransactionalUser.from_orm(transactional_user))


def generate_pin(db: Session, punto_venta_id: int) -> str:
    transactional_user_list: List[TransactionalUser] = service.get_list_by_filter(
        TransactionalUser,
        db,
        punto_venta_id=punto_venta_id,
    )
    duplicate_pin_found = True
    while duplicate_pin_found:
        duplicate_pin_found = False
        pin = str(randrange(1000, 9999))
        for user in transactional_user_list:
            if verify_pin(pin, user.pin):
                duplicate_pin_found = True
                break
    return pin


def send_pin_by_sms(telefono: str, pin: str):
    mensaje = f"iCargo * Su PIN para permitir el retiro de Ordenes de Carga y Lineas de Credito es: {pin} * NO COMPARTA este codigo con nadie."  # noqa: B950
    send_sms(telefono, mensaje)
