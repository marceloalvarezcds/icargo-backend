from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.Liquidacion])
async def read_liquidacion_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.LIQUIDACION)),  # noqa: B008
):
    return repositories.get_liquidacion_list(db)


@api.get(
    "/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}/etapa/{etapa}",  # noqa
    response_model=List[schemas.Liquidacion],
)
async def read_liquidacion_list_by_estado_cuenta(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    etapa: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.LIQUIDACION)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_liquidacion_list_by_estado_cuenta(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        etapa,
        current_user.gestor_carga_id,
    )


@api.get("/gestor_carga_id", response_model=List[schemas.Liquidacion])
async def read_liquidacion_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.LIQUIDACION)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_liquidacion_list(db, current_user.gestor_carga_id)


@api.get("/reports")
async def liquidacion_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.LIQUIDACION)),  # noqa: B008
):
    return services.get_liquidacion_reports(db)


@api.get(
    "/reports/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}/etapa/{etapa}"  # noqa
)
async def liquidacion_reports_by_estado_cuenta(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    etapa: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.LIQUIDACION)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_liquidacion_reports_by_estado_cuenta(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        etapa,
        current_user.gestor_carga_id,
    )


@api.get("/{id}/pdf/etapa/{etapa}")
def get_liquidacion_resumen_pdf_by_id(
    id: int,
    etapa: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.LIQUIDACION)),  # noqa: B008
):
    return services.get_liquidacion_resumen_pdf_by_id(db, id, etapa)


@api.get("/{id}", response_model=schemas.Liquidacion)
async def read_liquidacion_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.LIQUIDACION)),  # noqa: B008
):
    return services.get_liquidacion_by_id(db, id)


@api.post("/", response_model=schemas.Liquidacion)
async def add_new_liquidacion(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.LiquidacionAddMovimientosForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.create_liquidacion_pendiente(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Liquidacion)
async def edit_liquidacion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.LiquidacionForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.edit_liquidacion(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Liquidacion)
async def delete_liquidacion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.delete_liquidacion(db, id, current_user.username)


@api.patch("/{id}/add_movimientos", response_model=schemas.Liquidacion)
async def add_movimientos(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.LiquidacionAddMovimientosForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.MOVIMIENTO)),  # noqa: B008
    __: bool = Depends(Permiso(a.EDITAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.add_movimientos(id, db, data, current_user.username)  # type: ignore


@api.patch("/{id}/remove_movimiento", response_model=schemas.Liquidacion)
async def remove_movimiento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.Movimiento] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.MOVIMIENTO)),  # noqa: B008
    __: bool = Depends(Permiso(a.EDITAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.remove_movimiento(id, db, data, current_user.username)  # type: ignore


@api.get("/{id}/aceptar", response_model=schemas.Liquidacion)
async def aceptar_liquidacion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ACEPTAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.aceptar_liquidacion(db, id, current_user.username)


@api.get("/{id}/cancelar", response_model=schemas.Liquidacion)
async def cancelar_liquidacion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CANCELAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.cancelar_liquidacion(db, id, current_user.username)


@api.patch("/{id}/rechazar", response_model=schemas.Liquidacion)
async def rechazar_liquidacion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[str] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.RECHAZAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.rechazar_liquidacion(db, id, data, current_user)


@api.patch("/{id}/en_revision", response_model=schemas.Liquidacion)
async def en_revision_liquidacion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[str] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.PASAR_A_REVISION, m.LIQUIDACION)),  # noqa: B008
):
    return services.en_revision_liquidacion(db, id, data, current_user)


@api.patch("/{id}/add_instrumentos", response_model=schemas.Liquidacion)
async def add_instrumentos(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.LiquidacionAddInstrumentosForm] = Form(...),  # type: ignore  # noqa
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.INSTRUMENTO)),  # noqa: B008
    __: bool = Depends(Permiso(a.EDITAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.add_instrumentos(id, db, data, current_user.username)  # type: ignore
