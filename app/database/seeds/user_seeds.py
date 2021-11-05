from sqlalchemy.orm import Session  # type: ignore

from app.config import ENV, USER_ADMIN_PASS
from app.enums import CodigoRolEnum
from app.models import User
from app.repositories import rol, user
from app.utils.security import get_password_hash


def user_seeds(db: Session):
    admin_icargo_rol = rol.get_rol_by_codigo(db, CodigoRolEnum.ADMIN_ICARGO.value)
    admin_username = "admin-icargo"
    admin_user = user.get_by_username(db, admin_username)
    if admin_user is None:
        admin_user = User(
            token="",
            first_name="Icargo",
            last_name="Admin",
            username=admin_username,
            surname=admin_username,
            email="admin@icargo.com",
            is_activated=True,
            is_guest=False,
            is_superuser=True,
            password=get_password_hash(USER_ADMIN_PASS),
            roles=[admin_icargo_rol],
            modified_by="system",
        )
    db.add(admin_user)

    if ENV == "development":
        admin_suplente_icargo_rol = rol.get_rol_by_codigo(
            db, CodigoRolEnum.ADMIN_ICARGO.value
        )
        admin_suplente_username = "admin-suplente"
        admin_suplente_user = user.get_by_username(db, admin_suplente_username)
        if admin_suplente_user is None:
            admin_suplente_user = User(
                token=admin_suplente_username,
                first_name="Icargo",
                last_name="Admin",
                username=admin_suplente_username,
                surname=admin_suplente_username,
                email="admin-suplente@icargo.com",
                is_activated=True,
                is_guest=False,
                is_superuser=True,
                password=get_password_hash(USER_ADMIN_PASS),
                roles=[admin_suplente_icargo_rol],
                modified_by="system",
            )
        db.add(admin_suplente_user)

    db.commit()
