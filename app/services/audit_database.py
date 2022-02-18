from asyncio.log import logger
from datetime import timedelta
from typing import List

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.audits.audit_database import AuditDatabase as A
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums.estado import EstadoEnum
from app.models import OrdenCarga, OrdenCargaEstadoHistorial, User
from app.repositories.audit_database import (
    get_audit_list_by_table_filter_data_and_daterange,
)

from .permiso import check_permiso


def get_audit_list_by_orden_carga(
    db: Session, orden_carga: OrdenCarga, current_user: User
) -> List[A]:
    FINALIZADO = EstadoEnum.FINALIZADO.value
    if (orden_carga.estado == FINALIZADO) and check_permiso(
        current_user, m.ORDEN_CARGA, a.CONCILIAR
    ):
        estados: List[OrdenCargaEstadoHistorial] = orden_carga.historial
        finalizado = next((x for x in estados if x.estado == FINALIZADO), None)
        if finalizado:
            orden_carga_ids = [orden_carga.id]
            orden_carga_anticipo_retirado_ids = [x.id for x in orden_carga.anticipos]
            orden_carga_complemento_ids = [x.id for x in orden_carga.complementos]
            orden_carga_descuento_ids = [x.id for x in orden_carga.descuentos]
            orden_carga_remision_destino_ids = [
                x.id for x in orden_carga.remisiones_destino
            ]
            orden_carga_remision_origen_ids = [
                x.id for x in orden_carga.remisiones_origen
            ]
            start_date = finalizado.created_at - timedelta(seconds=2)
            logger.info(f"finalizado.created_at = {finalizado.created_at}")
            logger.info(f"start_date = {start_date}")
            conditions = [
                and_(
                    A.table_name == m.ORDEN_CARGA.value,
                    A.row_id.in_(orden_carga_ids),
                ).self_group(),
                and_(
                    A.table_name == m.ORDEN_CARGA_ANTICIPO_RETIRADO.value,
                    A.row_id.in_(orden_carga_anticipo_retirado_ids),
                ).self_group(),
                and_(
                    A.table_name == m.ORDEN_CARGA_COMPLEMENTO.value,
                    A.row_id.in_(orden_carga_complemento_ids),
                ).self_group(),
                and_(
                    A.table_name == m.ORDEN_CARGA_DESCUENTO.value,
                    A.row_id.in_(orden_carga_descuento_ids),
                ).self_group(),
                and_(
                    A.table_name == m.ORDEN_CARGA_REMISION_DESTINO.value,
                    A.row_id.in_(orden_carga_remision_destino_ids),
                ).self_group(),
                and_(
                    A.table_name == m.ORDEN_CARGA_REMISION_ORIGEN.value,
                    A.row_id.in_(orden_carga_remision_origen_ids),
                ).self_group(),
            ]
            return get_audit_list_by_table_filter_data_and_daterange(
                db, conditions, start_date
            )
        return []
    return []
