from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.EstadoCuenta])
async def read_estado_cuenta_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.ESTADO_CUENTA)),  # noqa: B008
):
    return services.get_estado_cuenta_list(db)


@api.get("/gestor_carga_id", response_model=List[schemas.EstadoCuenta])
async def read_estado_cuenta_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.ESTADO_CUENTA)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_estado_cuenta_list(db, current_user.gestor_carga_id)


@api.get(
    "/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}",  # noqa
    response_model=Optional[schemas.EstadoCuenta],
)
async def read_estado_cuenta_by_contraparte(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ESTADO_CUENTA)),  # noqa: B008
):
    return services.get_estado_cuenta_by_contraparte(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
    )


@api.get(
    "/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}/punto_venta_id/{punto_venta_id}",  # noqa
    response_model=Optional[schemas.EstadoCuenta],
)
async def read_estado_cuenta_by_contraparte(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    punto_venta_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ESTADO_CUENTA)),  # noqa: B008
):
    return services.get_estado_cuenta_by_contraparte(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        punto_venta_id
    )


@api.get("/reports")
async def estado_cuenta_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.ESTADO_CUENTA)),  # noqa: B008
):
    return services.get_estado_cuenta_reports(db)



# add nuevo servicio de estado de cuenta detallado aqui
@api.get(
    "/movimiento/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}",  # noqa
    response_model=List[schemas.MovimientoEstadoCuenta],
)
async def read_movimiento_list_by_estado_cuenta_det(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    punto_venta_id: Optional[int] = None,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_nuevo_servicio(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        current_user.gestor_carga_id,
        punto_venta_id
    )
