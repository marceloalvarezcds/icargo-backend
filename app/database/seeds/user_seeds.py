from sqlalchemy.orm import Session  # type: ignore

from app.config import USER_ADMIN_PASS
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
    db.commit()
