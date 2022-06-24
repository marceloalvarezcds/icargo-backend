from sqlalchemy.orm import Session  # type: ignore

from app.models.rol import Permiso, Rol, RolPermiso


def create_rol_permiso(
    db: Session,
    rol: Rol,
    permiso: Permiso,
    modified_by: str,
) -> RolPermiso:
    obj = RolPermiso(
        rol_id=rol.id,
        permiso_id=permiso.id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
