from typing import List, Optional

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import MovimientoEstadoEnum

api = APIRouter()


@api.get("/", response_model=List[schemas.Movimiento])
async def read_movimiento_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
):
    return repositories.get_movimiento_list(db)


@api.get("/reports")
async def movimiento_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.MOVIMIENTO)),  # noqa: B008
):
    return services.get_movimiento_reports(db)


@api.get(
    "/reports/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}/etapa/{etapa}",  # noqa: B950
)
async def get_movimiento_reports_by_estado(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    etapa: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.MOVIMIENTO)),  # noqa: B008,
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_movimiento_list_by_estado_cuenta(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        etapa,
        current_user.gestor_carga_id,
    )


@api.get("/reports/liquidacion/{liquidacion_id}/estado/{estado}")
async def movimiento_reports_by_estado_and_liquidacion_id(
    liquidacion_id: int,
    estado: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.MOVIMIENTO)),  # noqa: B008
):
    return services.get_movimiento_reports(db, liquidacion_id, estado)


@api.get("/gestor_carga_id", response_model=List[schemas.Movimiento])
async def read_movimiento_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_movimiento_list(db, current_user.gestor_carga_id)


@api.get("/reports/gestor_carga_id")
async def movimiento_reports_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.MOVIMIENTO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_movimiento_reports_by_gestor_carga_id(
        db, current_user.gestor_carga_id
    )


@api.get(
    "/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}",  # noqa
    response_model=List[schemas.MovimientoEstadoCuenta],
)
async def read_movimiento_list_by_estado_cuenta_det(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_all_movimiento_list_by_estado_cuenta(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        current_user.gestor_carga_id,
    )


@api.get(
    "/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}/etapa/{etapa}",  # noqa
    response_model=List[schemas.Movimiento],
)
async def read_movimiento_list_by_estado_cuenta(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    etapa: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_movimiento_list_by_estado_cuenta(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        etapa,
        current_user.gestor_carga_id,
    )


@api.get(
    "/liquidacion/{liquidacion_id}/etapa/{etapa}",
    response_model=List[schemas.Movimiento],
)
async def read_movimiento_list_by_liquidacion(
    liquidacion_id: int,
    etapa: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_movimiento_list_by_liquidacion(
        db,
        liquidacion_id,
        etapa,
        current_user.gestor_carga_id,
    )


@api.get("/orden_carga/{orden_carga_id}", response_model=List[schemas.Movimiento])
async def read_movimiento_list_by_orden_carga_id(
    orden_carga_id: int,  # noqa: B008
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
):
    return repositories.get_movimiento_list_by_orden_carga_id(db, orden_carga_id)


@api.get("/{id}", response_model=schemas.Movimiento)
async def read_movimiento_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.MOVIMIENTO)),  # noqa: B008
):
    return services.get_movimiento_by_id(db, id)


@api.post("/", response_model=Optional[schemas.Movimiento])
async def add_new_movimiento_by_tipo_documento_relacionado_otro(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MovimientoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.create_movimiento_by_tipo_documento_relacionado_otro(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Movimiento)
async def edit_movimiento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MovimientoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.edit_movimiento(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}/edit_by_gestor_flete", response_model=Optional[schemas.Movimiento])
async def edit_movimiento_by_gestor_flete(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MovimientoFleteEditForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.edit_movimiento_by_gestor_flete(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}/edit_by_gestor_merma", response_model=Optional[schemas.Movimiento])
async def edit_movimiento_by_gestor_merma(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MovimientoMermaEditForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.edit_movimiento_by_gestor_merma(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}/edit_by_propietario_flete", response_model=Optional[schemas.Movimiento])
async def edit_movimiento_by_propietario_flete(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MovimientoFleteEditForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.edit_movimiento_by_propietario_flete(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}/edit_by_propietario_merma", response_model=Optional[schemas.Movimiento])
async def edit_movimiento_by_propietario_merma(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MovimientoMermaEditForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.edit_movimiento_by_propietario_merma(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Movimiento)
async def delete_movimiento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.delete_movimiento(db, id, current_user.username)


@api.get(
    "/reports/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}",  # noqa: B950
)
async def get_movimiento_reports_by_estado(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.MOVIMIENTO)),  # noqa: B008,
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_movimiento_estado_cuenta_reports_by_contraparte(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        current_user.gestor_carga_id,
    )


@api.get(
    "/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}/punto_venta_id/{punto_venta_id}",  # noqa
    response_model=List[schemas.MovimientoEstadoCuenta],
)
async def read_movimiento_list_by_estado_cuenta_det(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    punto_venta_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_all_movimiento_list_by_estado_cuenta(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        current_user.gestor_carga_id,
        punto_venta_id
    )


@api.get(
    "/tipo_contraparte/{tipo_contraparte_id}/id/{contraparte_id}/contraparte/{contraparte}/numero_documento/{contraparte_numero_documento}/etapa/{etapa}/punto_venta_id/{punto_venta_id}",  # noqa
    response_model=List[schemas.Movimiento],
)
async def read_movimiento_list_by_estado_cuenta(
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    etapa: str,
    punto_venta_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_movimiento_list_by_estado_cuenta(
        db,
        tipo_contraparte_id,
        contraparte_id,
        contraparte,
        contraparte_numero_documento,
        etapa,
        current_user.gestor_carga_id,
        punto_venta_id
    )
