from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.OrdenCargaList])
async def read_orden_carga_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.get_orden_carga_list(db, current_user.gestor_carga_id)


@api.get("/reports")
async def orden_carga_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.get_orden_carga_reports(db, current_user.gestor_carga_id)


@api.get("/{id}", response_model=schemas.OrdenCarga)
async def read_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.get_orden_carga_detail(db, id, current_user)


@api.post("/", response_model=schemas.OrdenCarga)
async def add_new_orden_carga(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.create_orden_carga(
        db,
        data,  # type: ignore
        current_user,
    )


@api.put("/{id}", response_model=schemas.OrdenCarga)
async def edit_orden_carga(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaEditForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.edit_orden_carga(
        id,
        db,
        data,  # type: ignore
        current_user,
    )


@api.delete("/{id}", response_model=schemas.OrdenCarga)
async def delete_orden_carga(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.delete_orden_carga(db, id, current_user)


@api.get("/{id}/pdf")
def read_orden_carga_pdf_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.get_orden_carga_pdf_by_id(db, id)


@api.get("/{id}/pdf/resumen")
def read_orden_carga_resumen_pdf_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.get_orden_carga_resumen_pdf_by_id(db, id)


@api.get("/{id}/aceptar", response_model=schemas.OrdenCarga)
def aceptar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.aceptar_orden_carga(db, id, current_user)


@api.get("/{id}/cancelar", response_model=schemas.OrdenCarga)
def cancelar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.cancelar_orden_carga(db, id, current_user)


@api.get("/{id}/conciliar", response_model=schemas.OrdenCarga)
def conciliar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.conciliar_orden_carga(db, id, current_user)


@api.get("/{id}/contabilizar", response_model=schemas.OrdenCarga)
def contabilizar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.contabilizar_orden_carga(db, id, current_user)


@api.get("/{id}/arribado_a_cargar", response_model=schemas.OrdenCarga)
def arribado_a_cargar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.arribado_a_cargar_orden_carga(db, id, current_user)


@api.get("/{id}/arribado_a_descargar", response_model=schemas.OrdenCarga)
def arribado_a_descargar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.arribado_a_descargar_orden_carga(db, id, current_user)


@api.get("/{id}/cargar", response_model=schemas.OrdenCarga)
def cargar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.cargar_orden_carga(db, id, current_user)


@api.get("/{id}/descargar", response_model=schemas.OrdenCarga)
def descargar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.descargar_orden_carga(db, id, current_user)


@api.get("/{id}/finalizar", response_model=schemas.OrdenCarga)
def finalizar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.finalizar_orden_carga(db, id, current_user)


@api.get("/{id}/liquidar", response_model=schemas.OrdenCarga)
def liquidar_orden_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.liquidar_orden_carga(db, id, current_user)


@api.get("/{id}/modify_advance_release", response_model=schemas.OrdenCarga)
def modify_advance_release(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.change_orden_carga_anticipos_liberados(db, id, current_user)
