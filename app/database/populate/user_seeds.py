from sqlalchemy.orm import Session  # type: ignore

from app.database.seeds.permiso_seeds import (
    gestor_icargo_permiso_seeds,
    gestor_suplente_icargo_permiso_seeds,
)
from app.database.seeds.user_rol_seeds import user_rol_seeds
from app.enums import CodigoRolEnum
from app.models import GestorCarga, User
from app.services import get_user_by_username
from app.utils.security import get_password_hash


def user_seeds(
    db: Session,
    username: str,
    first_name: str,
    last_name: str,
    gestor_carga: GestorCarga,
):
    usuario = get_user_by_username(db, username)
    email = f"{first_name.replace(' ', '-').lower()}@{last_name.replace(' ', '-').lower()}.com"
    if usuario is None:
        usuario = User(
            token=username,
            first_name=first_name,
            last_name=last_name,
            username=username,
            surname=username,
            email=email,
            is_superuser=False,
            password=get_password_hash(username),
            gestor_carga_id=gestor_carga.id,
        )
        db.add(usuario)
        db.commit()
    if "suplente" in username:
        permisos = gestor_suplente_icargo_permiso_seeds(db)
        rol = CodigoRolEnum.SUPLENTE_GESTOR_CARGA.value
    else:
        permisos = gestor_icargo_permiso_seeds(db)
        rol = CodigoRolEnum.ADMIN_GESTOR_CARGA.value
    user_rol_seeds(
        db,
        usuario,
        rol,
        permisos,
        gestor_carga.id,
    )
