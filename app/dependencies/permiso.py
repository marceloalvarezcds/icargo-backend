from typing import List

from fastapi import Depends, HTTPException, status

from app import models
from app.dependencies import get_current_user
from app.enums import PermisoAccionEnum, PermisoModeloEnum


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
        self, current_user: models.User = Depends(get_current_user)  # noqa: B008
    ):
        permisos: List[models.Permiso] = current_user.permisos
        for permiso in permisos:
            if (
                permiso.modelo == self.modelo.value
                and permiso.accion == self.accion.value
            ):
                return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para realizar la acción",
        )
