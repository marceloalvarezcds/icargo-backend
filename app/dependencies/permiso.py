from http import HTTPStatus
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session  # type: ignore

from app import schemas
from app.cache import check_permiso_in_cache, get_permiso_in_cache, set_permiso_in_cache
from app.dependencies import get_current_user, get_db_session
from app.enums import PermisoAccionEnum, PermisoModeloEnum, permisoModeloTitulo
from app.repositories import exists_permiso_for_user

class Permiso:
    """
    Clase para controlar los permisos para en cada endpoint
    """

    accion: PermisoAccionEnum
    modelo: PermisoModeloEnum

    def __init__(
        self,
        accion: PermisoAccionEnum,
        modelo: PermisoModeloEnum,
    ):
        self.modelo = modelo
        self.accion = accion

    def __call__(
        self,
        db: Session = Depends(get_db_session),  # noqa: B008
        current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    ):
        if current_user:
            accion = self.accion
            modelo = self.modelo
            user_id = current_user.id
            # Si permiso en cache es None entonces busca en base de datos
            if check_permiso_in_cache(user_id, accion, modelo) is None:
                has_permiso_in_db = (
                    exists_permiso_for_user(db, user_id, accion, modelo) > 0
                )
                set_permiso_in_cache(user_id, accion, modelo, has_permiso_in_db)
                if has_permiso_in_db:
                    return True
            else:
                # Si encontró permiso en la cache retorna el valor solo en caso de ser verdadero
                has_permiso_in_cache = get_permiso_in_cache(user_id, accion, modelo)
                if has_permiso_in_cache:
                    return True
            # En caso de no encontrar permiso en cache o base de datos mostrar mensaje de error al usuario  # noqa: B950
            modelt = permisoModeloTitulo[modelo.value]
            action = " ".join(str(accion.value).split("_")).capitalize()
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, #mejorar en algun momento
                # status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permiso para {action} {modelt}",
            )
        return False
