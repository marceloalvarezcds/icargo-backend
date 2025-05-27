
from typing import List, Optional
from sqlalchemy.orm import Query, Session # type: ignore
from sqlalchemy.orm import  Session # type: ignore
from sqlalchemy import case, null
from app.enums import (
    MovimientoEstadoEnum
)
from sqlalchemy.sql.elements import and_, or_, literal_column # type: ignore
from app.models import (
    TipoCuenta,
    Provision,
    Moneda
)
from app.schemas import ProvisionForm


def get_provision_list(db: Session) -> List[Provision]:
    return (
        db.query(Provision)
        .filter(Provision.estado != MovimientoEstadoEnum.ELIMINADO.value)
        .order_by(Provision.id, Provision.contraparte, )
        .all()
    )

def create_provision(
    db: Session,
    data: ProvisionForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Provision:
    obj = Provision(
        gestor_carga_id=gestor_carga_id,
        orden_carga_id=data.orden_carga_id,
        tipo_contraparte_id=data.tipo_contraparte_id,
        contraparte=data.contraparte,
        contraparte_numero_documento=data.contraparte_numero_documento,
        tipo_documento_relacionado_id=data.tipo_documento_relacionado_id,
        numero_documento_relacionado=data.numero_documento_relacionado,
        cuenta_id=data.cuenta_id,
        tipo_movimiento_id=data.tipo_movimiento_id,
        #es_editable=data.es_editable,
        estado=data.estado.value,
        fecha=data.fecha,
        detalle=data.detalle,
        monto=data.monto,
        moneda_id=data.moneda_id,
        tipo_cambio_moneda=data.tipo_cambio_moneda,
        fecha_cambio_moneda=data.fecha_cambio_moneda,
        # En caso de ser movimiento de anticipo
        anticipo_id=data.anticipo_id,
        # En caso de ser movimiento de complemento o descuento
        complemento_id=data.complemento_id,
        descuento_id=data.descuento_id,
        # IDs para referencia a las tablas de las contraparte
        chofer_id=data.chofer_id,
        propietario_id=data.propietario_id,
        proveedor_id=data.proveedor_id,
        remitente_id=data.remitente_id,
        created_by=modified_by,
        modified_by=modified_by,
        tipo_movimiento_info=data.tipo_movimiento_info,
        punto_venta_id=data.punto_venta_id,
        linea_movimiento=data.linea_movimiento
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_query_provisiones_by_contraparte_and_gestor_carga_id(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    gestor_carga_id: int,
    punto_venta_id: Optional[int]
    ) -> Query:

    # columnas especificas
    query = db.query(
                literal_column("1").label("orden"),
                Provision.id.label("movimiento_id"),
                literal_column("0").label("instrumento_id"),
                null().label("liquidacion_id"),
                literal_column("' '").label("contraparte_alias"),
                Provision.created_at.label("fecha"),
                TipoCuenta.descripcion.label("tipo_cuenta_descripcion"),
                literal_column("'Provision'").label("tipo_movimiento_concepto"),
                Provision.tipo_movimiento_info.label("detalle"),
                Provision.orden_carga_id.label("nro_documento_relacionado"),
                Provision.detalle.label("info"),
                Provision.estado.label("estado"),
                null().label("estado_liquidacion"),
                literal_column("false").label("es_editable"),
                literal_column("false").label("can_edit_oc"),
                literal_column("false").label("documento_fisico"),
                Moneda.simbolo.label("moneda"),
                Provision.tipo_cambio_moneda.label("tipo_cambio_moneda"),
                case(
                    (
                        Provision.moneda_id == 1,
                        Provision.monto,
                    ),
                    else_= Provision.monto*Provision.tipo_cambio_moneda,
                ).label("provision"),
                literal_column("0").label("pendiente"),
                literal_column("0").label("en_proceso"),
                literal_column("0").label("confirmado"),
                literal_column("0").label("finalizado"),
                )\
                .join(Provision.tipo_movimiento)\
                .join(Provision.cuenta)\
                .join(Provision.moneda)\

    query = query.filter(
            and_(
                Provision.tipo_contraparte_id == tipo_contraparte_id,
                or_(
                    Provision.propietario_id == contraparte_id,
                    Provision.remitente_id == contraparte_id,
                    Provision.proveedor_id == contraparte_id,
                    and_(
                        Provision.contraparte == contraparte,
                        Provision.contraparte_numero_documento
                        == contraparte_numero_documento,
                    ),
                    Provision.chofer_id == contraparte_id,
                ),
                or_(
                    # OrdenCargaAnticipoRetirado.punto_venta_id == punto_venta_id,
                    Provision.punto_venta_id == punto_venta_id,
                    punto_venta_id == None
                ),
                Provision.gestor_carga_id == gestor_carga_id
            )
        )
    return query
