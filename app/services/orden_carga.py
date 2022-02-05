import os

from fastapi import HTTPException
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.config import REPORTS_FOLDER
from app.enums import EstadoEnum
from app.models import Flete, OrdenCarga, User
from app.utils.meta_inspect import get_dict

from .orden_carga_anticipo_saldo import get_orden_carga_by_id
from .orden_carga_complemento_flete import create_orden_carga_complemento_by_flete
from .orden_carga_descuento_flete import create_orden_carga_descuento_by_flete
from .orden_carga_remision_resultado import (
    get_orden_carga_remision_resultado_list_by_orden_carga,
)


def get_orden_carga_with_resultado(
    model: OrdenCarga, current_user: User
) -> schemas.OrdenCarga:
    obj_dict = get_dict(model, ignore_keys=["orden_carga"], for_json=False)
    obj_dict[
        "remisiones_resultado"
    ] = get_orden_carga_remision_resultado_list_by_orden_carga(model, current_user)
    return schemas.OrdenCarga.parse_obj(obj_dict)


def create_complementos_and_descuentos(
    db: Session, obj: OrdenCarga, flete: Flete, modified_by: str
):
    for c in flete.complementos:
        create_orden_carga_complemento_by_flete(db, obj, c, modified_by)
    for d in flete.descuentos:
        create_orden_carga_descuento_by_flete(db, obj, d, modified_by)


def create_orden_carga(
    db: Session,
    data: schemas.OrdenCargaForm,
    current_user: User,
) -> schemas.OrdenCarga:
    flete = repositories.get_flete_by_id(db, data.flete_id)
    if not flete:
        raise HTTPException(status_code=404, detail="Flete no encontrado")
    modified_by = current_user.username
    obj = repositories.create_orden_carga(
        db,
        data,
        flete,
        current_user.gestor_carga_id,
        modified_by,
    )
    create_complementos_and_descuentos(db, obj, flete, modified_by)
    return get_orden_carga_with_resultado(obj, current_user)


def edit_orden_carga(
    id: int,
    db: Session,
    data: schemas.OrdenCargaEditForm,
    current_user: User,
) -> schemas.OrdenCarga:
    to_edit_obj = get_orden_carga_by_id(db, id)
    obj = repositories.edit_orden_carga(
        to_edit_obj,
        db,
        data,
        current_user.gestor_carga_id,
        current_user.username,
    )
    return get_orden_carga_with_resultado(obj, current_user)


def delete_orden_carga(db: Session, id: int, current_user: User) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.delete_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def get_orden_carga_detail(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    return get_orden_carga_with_resultado(obj, current_user)


def change_orden_carga_anticipos_liberados(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    if not obj.anticipos_liberados and obj.estado == EstadoEnum.CANCELADO.value:
        raise HTTPException(
            status_code=403,
            detail="La orden de carga ya está cancelada, no puede liberar anticipos",
        )
    anticipos_liberados = not obj.anticipos_liberados
    model = repositories.change_orden_carga_anticipos_liberados(
        obj, db, anticipos_liberados, current_user.username
    )
    return get_orden_carga_with_resultado(model, current_user)


def aceptar_orden_carga(db: Session, id: int, current_user: User) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.aceptar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def cancelar_orden_carga(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.cancelar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def conciliar_orden_carga(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.conciliar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def contabilizar_orden_carga(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.contabilizar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def arribado_a_cargar_orden_carga(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.arribado_a_cargar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def arribado_a_descargar_orden_carga(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.arribado_a_descargar_orden_carga(
        obj, db, current_user.username
    )
    return get_orden_carga_with_resultado(model, current_user)


def cargar_orden_carga(db: Session, id: int, current_user: User) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.cargar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def descargar_orden_carga(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.descargar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def finalizar_orden_carga(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.finalizar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def liquidar_orden_carga(
    db: Session, id: int, current_user: User
) -> schemas.OrdenCarga:
    obj = get_orden_carga_by_id(db, id)
    model = repositories.liquidar_orden_carga(obj, db, current_user.username)
    return get_orden_carga_with_resultado(model, current_user)


def get_orden_carga_reports(db: Session) -> str:
    datalist = repositories.get_orden_carga_list(db)
    wb = Workbook()
    # get worksheet
    ws = wb.active

    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "Nº"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=2)
    title_cell.value = "Estado"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=3)
    title_cell.value = "Estado Anticipos"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=4)
    title_cell.value = "Nº Pedido"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=5)
    title_cell.value = "Placa Camión"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=6)
    title_cell.value = "Placa Semirrelque"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=7)
    title_cell.value = "Cant. Nominada (kg)"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=8)
    title_cell.value = "Comentarios"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=9)
    title_cell.value = "Gestora de Carga"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=10)
    title_cell.value = "Remisiones"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=11)
    title_cell.value = "Nº Ticket"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=12)
    title_cell.value = "Remitente"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=13)
    title_cell.value = "Chofer"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=14)
    title_cell.value = "Propietario"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=15)
    title_cell.value = "Tipo de Flete"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=16)
    title_cell.value = "Producto"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=17)
    title_cell.value = "Origen"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=18)
    title_cell.value = "Destino"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=19)
    title_cell.value = "Cant. Origen (kg)"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=20)
    title_cell.value = "Cant. Destino (kg)"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=21)
    title_cell.value = "Lugar de Carga"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=22)
    title_cell.value = "Lugar de Descarga"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=23)
    title_cell.value = "Usuario creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=24)
    title_cell.value = "Fecha creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=25)
    title_cell.value = "Usuario modificación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=26)
    title_cell.value = "Fecha modificación"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):
        value_cell = ws.cell(row=row + 2, column=1)
        value_cell.value = item.id

        value_cell = ws.cell(row=row + 2, column=2)
        value_cell.value = item.estado

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.anticipos_liberados_descripcion

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = item.flete_id

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.camion_placa

        value_cell = ws.cell(row=row + 2, column=6)
        value_cell.value = item.semi_placa

        value_cell = ws.cell(row=row + 2, column=7)
        value_cell.value = item.cantidad_nominada

        value_cell = ws.cell(row=row + 2, column=8)
        value_cell.value = item.comentarios

        value_cell = ws.cell(row=row + 2, column=9)
        value_cell.value = item.gestor_carga_nombre

        value_cell = ws.cell(row=row + 2, column=10)
        value_cell.value = item.remisiones

        value_cell = ws.cell(row=row + 2, column=11)
        value_cell.value = item.nro_tickets

        value_cell = ws.cell(row=row + 2, column=12)
        value_cell.value = item.flete_remitente_nombre

        value_cell = ws.cell(row=row + 2, column=13)
        value_cell.value = item.camion_chofer_nombre

        value_cell = ws.cell(row=row + 2, column=14)
        value_cell.value = item.camion_propietario_nombre

        value_cell = ws.cell(row=row + 2, column=15)
        value_cell.value = item.flete_tipo

        value_cell = ws.cell(row=row + 2, column=16)
        value_cell.value = item.flete_producto_descripcion

        value_cell = ws.cell(row=row + 2, column=17)
        value_cell.value = item.flete_origen_nombre

        value_cell = ws.cell(row=row + 2, column=18)
        value_cell.value = item.flete_destino_nombre

        value_cell = ws.cell(row=row + 2, column=19)
        value_cell.value = item.cantidad_origen

        value_cell = ws.cell(row=row + 2, column=20)
        value_cell.value = item.cantidad_destino

        value_cell = ws.cell(row=row + 2, column=21)
        value_cell.value = item.origen_nombre

        value_cell = ws.cell(row=row + 2, column=22)
        value_cell.value = item.destino_nombre

        value_cell = ws.cell(row=row + 2, column=23)
        value_cell.value = item.created_by

        value_cell = ws.cell(row=row + 2, column=24)
        value_cell.value = item.created_at

        value_cell = ws.cell(row=row + 2, column=25)
        value_cell.value = item.modified_by

        value_cell = ws.cell(row=row + 2, column=26)
        value_cell.value = item.modified_at

    ws.auto_filter.ref = ws.dimensions
    filename = "orden_carga_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
