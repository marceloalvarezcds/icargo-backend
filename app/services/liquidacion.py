import os
from typing import List, Optional

from fastapi import HTTPException  # type: ignore
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.config import REPORTS_FOLDER
from app.enums import EstadoEnum, TipoContraparteEnum
from app.models import Liquidacion, Movimiento
from app.schemas import LiquidacionCreateForm, LiquidacionForm


def get_liquidacion_list(
    db: Session, gestor_carga_id: Optional[int]
) -> List[Liquidacion]:
    if gestor_carga_id:
        return repositories.get_liquidacion_list_by_gestor_carga_id(db, gestor_carga_id)
    return repositories.get_liquidacion_list(db)


def create_liquidacion(
    db: Session,
    data: LiquidacionForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Liquidacion:
    gestor_id = gestor_carga_id if gestor_carga_id else data.gestor_carga_id
    if not gestor_id:
        raise HTTPException(status_code=409, detail="Debe elegir un Gestor de carga")
    return repositories.create_liquidacion(db, data, gestor_id, modified_by)


def create_liquidacion_pendiente(
    db: Session,
    data: LiquidacionCreateForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Movimiento:
    mList = data.movimientos
    if len(mList) == 0:
        raise HTTPException(
            status_code=409, detail="Debe elegir al menos un movimiento"
        )
    movimientos: List[Movimiento] = []
    for m in mList:
        mov = repositories.get_movimiento_by_id(db, m.id)
        if mov:
            mov.estado = EstadoEnum.EN_PROCESO.value
            movimientos.append(mov)
    movimiento = movimientos[0]
    gestor_id = gestor_carga_id if gestor_carga_id else movimiento.gestor_carga_id
    if not gestor_id:
        raise HTTPException(status_code=409, detail="Debe elegir un Gestor de carga")
    chofer_id = None
    propietario_id = None
    proveedor_id = None
    remitente_id = None
    if movimiento.tipo_contraparte_descripcion == TipoContraparteEnum.CHOFER:
        chofer_id = movimiento.chofer_id
    elif movimiento.tipo_contraparte_descripcion == TipoContraparteEnum.PROVEEDOR:
        proveedor_id = movimiento.proveedor_id
    elif movimiento.tipo_contraparte_descripcion == TipoContraparteEnum.REMITENTE:
        remitente_id = movimiento.remitente_id
    else:
        propietario_id = movimiento.propietario_id
    liquidacion = create_liquidacion(
        db,
        LiquidacionForm(
            tipo_contraparte_id=movimiento.tipo_contraparte_id,
            contraparte=movimiento.contraparte,
            contraparte_numero_documento=movimiento.contraparte_numero_documento,
            moneda_id=movimiento.moneda_id,
            # IDs para referencia a las tablas de las contraparte
            chofer_id=chofer_id,
            gestor_carga_id=gestor_carga_id,
            propietario_id=propietario_id,
            proveedor_id=proveedor_id,
            remitente_id=remitente_id,
        ),
        gestor_id,
        modified_by,
    )
    liquidacion.movimientos = movimientos
    db.commit()
    return liquidacion


def get_liquidacion_by_id(db: Session, id: int) -> Liquidacion:
    obj = repositories.get_liquidacion_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Liquidacion no encontrado")
    return obj


def edit_liquidacion(
    id: int,
    db: Session,
    data: LiquidacionForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Liquidacion:
    gestor_id = gestor_carga_id if gestor_carga_id else data.gestor_carga_id
    if not gestor_id:
        raise HTTPException(status_code=409, detail="Debe elegir un Gestor de carga")
    to_edit_obj = get_liquidacion_by_id(db, id)
    return repositories.edit_liquidacion(to_edit_obj, db, data, gestor_id, modified_by)


def delete_liquidacion(db: Session, id: int, modified_by: str) -> Liquidacion:
    co = get_liquidacion_by_id(db, id)
    return repositories.delete_liquidacion(co, db, modified_by)


def get_liquidacion_reports(db: Session) -> str:
    datalist = repositories.get_liquidacion_list(db)
    wb = Workbook()
    ws = wb.active

    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "ID"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=2)
    title_cell.value = "Fecha Aprobación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=3)
    title_cell.value = "Aprobador por"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=4)
    title_cell.value = "Tipo de Contraparte"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=5)
    title_cell.value = "Nombre Contraparte"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=6)
    title_cell.value = "Nº Contraparte"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=7)
    title_cell.value = "Cobro/Pago"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=8)
    title_cell.value = "Moneda"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=9)
    title_cell.value = "Valor de operación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=10)
    title_cell.value = "Valor de instrumento"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=11)
    title_cell.value = "Residuo"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=12)
    title_cell.value = "Estado"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=13)
    title_cell.value = "Fecha de Pago/Cobro"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=14)
    title_cell.value = "Fecha modificación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=15)
    title_cell.value = "Usuario modificación"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):
        value_cell = ws.cell(row=row + 2, column=1)
        value_cell.value = item.id

        value_cell = ws.cell(row=row + 2, column=2)
        value_cell.value = item.created_by

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.created_at

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = item.tipo_contraparte_descripcion

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.contraparte

        value_cell = ws.cell(row=row + 2, column=6)
        value_cell.value = item.contraparte_numero_documento

        value_cell = ws.cell(row=row + 2, column=7)
        value_cell.value = item.tipo_operacion_descripcion

        value_cell = ws.cell(row=row + 2, column=8)
        value_cell.value = item.moneda_nombre

        value_cell = ws.cell(row=row + 2, column=9)
        value_cell.value = item.movimientos_saldo

        value_cell = ws.cell(row=row + 2, column=10)
        value_cell.value = item.instrumentos_saldo

        value_cell = ws.cell(row=row + 2, column=11)
        value_cell.value = item.saldo_residual

        value_cell = ws.cell(row=row + 2, column=12)
        value_cell.value = item.estado

        value_cell = ws.cell(row=row + 2, column=13)
        value_cell.value = item.fecha_pago_cobro

        value_cell = ws.cell(row=row + 2, column=14)
        value_cell.value = item.modified_by

        value_cell = ws.cell(row=row + 2, column=15)
        value_cell.value = item.modified_at

    ws.auto_filter.ref = ws.dimensions
    filename = "liquidacion_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
