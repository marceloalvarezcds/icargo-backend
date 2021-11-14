from sqlalchemy.orm import Session  # type: ignore

from app.database.seeds.permiso_seeds import entities_permiso_seeds
from app.enums import CodigoRolEnum
from app.models import GestorCarga, User
from app.repositories import rol, user
from app.utils.security import get_password_hash


def user_seeds(
    db: Session,
    username: str,
    first_name: str,
    last_name: str,
    gestor_carga: GestorCarga,
):
    admin_gestor_rol = rol.get_rol_by_codigo(db, CodigoRolEnum.ADMIN_GESTOR_CARGA.value)
    usuario = user.get_by_username(db, username)
    email = f"{first_name.replace(' ', '-').lower()}@{last_name.replace(' ', '-').lower()}.com"
    if usuario is None:
        usuario = User(
            token=username,
            first_name=first_name,
            last_name=last_name,
            username=username,
            surname=username,
            email=email,
            is_activated=True,
            is_guest=False,
            is_superuser=False,
            password=get_password_hash(username),
            gestor_carga_id=gestor_carga.id,
            roles=[admin_gestor_rol],
        )
        db.add(usuario)
        db.commit()
        entities_permiso_seeds(db, usuario)
