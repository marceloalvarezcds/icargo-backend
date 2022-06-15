from sqlalchemy.orm import Session  # type: ignore

from app.config import ENV, USER_ADMIN_PASS
from app.database.seeds.permiso_seeds import (
    entities_permiso_seeds,
    estado_cuenta_gestor_permiso_seeds,
    flete_permiso_seeds,
    flota_permiso_seeds,
    listado_permiso_seeds,
    orden_carga_gestor_permiso_seeds,
)
from app.enums import CodigoRolEnum
from app.models import User
from app.repositories import (
    get_gestor_carga_by,
    get_tipo_documento_by_descripcion,
    get_user_by_username,
    rol,
)
from app.utils.security import get_password_hash

from .permiso_seeds import admin_icargo_permiso_seeds


def user_seeds(db: Session):
    admin_icargo_rol = rol.get_rol_by_codigo(db, CodigoRolEnum.ADMIN_ICARGO.value)
    admin_username = "admin-icargo"
    admin_user = get_user_by_username(db, admin_username)
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
    admin_icargo_permiso_seeds(db, admin_user)

    tipo_documento = get_tipo_documento_by_descripcion(db, "RUC")
    if tipo_documento:
        gestor_carga_numero_documento = "80015858"
        gestor_carga = get_gestor_carga_by(
            db, tipo_documento.id, gestor_carga_numero_documento
        )
        if gestor_carga:
            admin_gestor_rol = rol.get_rol_by_codigo(
                db, CodigoRolEnum.ADMIN_GESTOR_CARGA.value
            )
            admin_gestor_username = "admin-transred"
            admin_gestor_user = get_user_by_username(db, admin_gestor_username)
            if admin_gestor_user is None:
                first_name = "Admin"
                last_name = "Transred"
                email = "transred@transred.com.py"
                admin_gestor_user = User(
                    token=admin_gestor_username,
                    first_name=first_name,
                    last_name=last_name,
                    username=admin_gestor_username,
                    surname=admin_gestor_username,
                    email=email,
                    is_activated=True,
                    is_guest=False,
                    is_superuser=False,
                    password=get_password_hash(f"{admin_gestor_username}-7176"),
                    gestor_carga_id=gestor_carga.id,
                    roles=[admin_gestor_rol],
                )
                db.add(admin_gestor_user)
                db.commit()
            entities_permiso_seeds(db, admin_gestor_user)
            flete_permiso_seeds(db, admin_gestor_user)
            flota_permiso_seeds(db, admin_gestor_user)
            orden_carga_gestor_permiso_seeds(db, admin_gestor_user)
            estado_cuenta_gestor_permiso_seeds(db, admin_gestor_user)
            listado_permiso_seeds(db, admin_gestor_user)

    if ENV == "development":
        admin_suplente_icargo_rol = rol.get_rol_by_codigo(
            db, CodigoRolEnum.ADMIN_ICARGO.value
        )
        admin_suplente_username = "admin-suplente"
        admin_suplente_user = get_user_by_username(db, admin_suplente_username)
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
                password=get_password_hash(admin_suplente_username),
                roles=[admin_suplente_icargo_rol],
                modified_by="system",
            )
            db.add(admin_suplente_user)
            db.commit()
        admin_icargo_permiso_seeds(db, admin_suplente_user)
