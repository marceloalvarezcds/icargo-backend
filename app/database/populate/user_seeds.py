from sqlalchemy.orm import Session  # type: ignore

from app.enums import CodigoRolEnum
from app.models import GestorCarga, User
from app.repositories import rol, user
from app.utils.security import get_password_hash


def user_seeds(db: Session, gestor_carga: GestorCarga):
    admin_gestor_rol = rol.get_rol_by_codigo(db, CodigoRolEnum.ADMIN_GESTOR_CARGA.value)
    transred_admin_username = "admin-transred"
    transred_admin_user = user.get_by_username(db, transred_admin_username)
    if transred_admin_user is None:
        transred_admin_user = User(
            token=transred_admin_username,
            first_name="Transred",
            last_name="Admin",
            username=transred_admin_username,
            surname=transred_admin_username,
            email="admin@transred.com",
            is_activated=True,
            is_guest=False,
            is_superuser=False,
            password=get_password_hash(transred_admin_username),
            gestor_carga_id=gestor_carga.id,
            roles=[admin_gestor_rol],
            modified_by="system",
        )
        db.add(transred_admin_user)
        db.commit()
