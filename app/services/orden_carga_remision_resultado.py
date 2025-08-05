from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import OrdenCarga
from app.schemas import OrdenCargaRemisionResultado
from app.services.permiso import check_permiso
from decimal import Decimal, ROUND_DOWN

def truncate(value, decimals=2):
    return float(Decimal(value).quantize(Decimal(f"1.{'0'*decimals}"), rounding=ROUND_DOWN))

def get_orden_carga_remision_resultado_list_by_orden_carga(
    db: Session, orden_carga: OrdenCarga, user_id: int
) -> List[OrdenCargaRemisionResultado]:
    lista: List[OrdenCargaRemisionResultado] = []
    # if check_permiso(db, user_id, m.ORDEN_CARGA_REMISION_RESULTADO, a.LISTAR, u.OC):
    if check_permiso(
            db, user_id, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR, a.VER, u.OC
        ):
            lista.append(
                OrdenCargaRemisionResultado(
                    responsable="Gestor de Carga",
                    tarifa_flete=orden_carga.resultado_gestor_carga_tarifa_flete,
                    total_flete=orden_carga.resultado_gestor_carga_total_flete,
                    merma_valor=orden_carga.merma_gestor_carga_valor,
                    tolerancia=orden_carga.merma_gestor_carga_tolerancia,
                    tolerancia_kg=orden_carga.resultado_gestor_carga_tolerancia_kg,
                    merma=orden_carga.resultado_gestor_carga_merma,
                    merma_valor_total=orden_carga.resultado_gestor_carga_merma_valor_total,
                    merma_valor_total_moneda_local=(
                        truncate(orden_carga.resultado_gestor_carga_merma_valor_total_moneda_local)
                    ),

                    saldo=truncate(orden_carga.resultado_gestor_carga_total_flete_saldo_bruto),
                    saldo_bruto=truncate(orden_carga.resultado_gestor_carga_total_flete_saldo_bruto),
                    complemento_descuento = truncate(orden_carga.resultado_gestor_carga_complemento_descuento),
                    # resultado_gestor_carga_saldo (calculo anterior),
                )
            )
    if check_permiso(db, user_id, m.ORDEN_CARGA_REMISION_RESULTADO_PROPIETARIO, a.VER, u.OC):
        lista.append(
            OrdenCargaRemisionResultado(
                responsable="Propietario",
                tarifa_flete=orden_carga.resultado_propietario_tarifa_flete,
                total_flete=orden_carga.resultado_propietario_total_flete,
                merma_valor=orden_carga.merma_propietario_valor,
                tolerancia=orden_carga.merma_propietario_tolerancia,
                tolerancia_kg=orden_carga.resultado_propietario_tolerancia_kg,
                merma=orden_carga.resultado_propietario_merma,
                merma_valor_total=orden_carga.resultado_propietario_merma_valor_total,
                merma_valor_total_moneda_local=(
                    truncate(orden_carga.resultado_propietario_merma_valor_total_moneda_local)
                ),
                total_complemento=orden_carga.resultado_propietario_total_complemento,
                total_descuento=orden_carga.resultado_propietario_total_descuento,
                total_anticipo=orden_carga.resultado_propietario_total_anticipos_retirados,
                saldo= truncate(orden_carga.resultado_propietario_saldo),
                total_efectivo= truncate(orden_carga.resultado_propietario_total_anticipos_retirados_efectivo),
                total_combustible= truncate(orden_carga.resultado_propietario_total_anticipos_retirados_combustible),
                saldo_bruto= truncate(orden_carga.resultado_propietario_saldo_bruto),
                complemento_descuento = truncate(orden_carga.resultado_propietario_complemento_descuento),
            )
        )
    return lista


def get_orden_carga_remision_resultado_list_by_flete(
    db: Session, orden_carga: OrdenCarga, user_id: int
) -> List[OrdenCargaRemisionResultado]:
    lista: List[OrdenCargaRemisionResultado] = []
    # if check_permiso(db, user_id, m.ORDEN_CARGA_REMISION_RESULTADO, a.LISTAR, u.OC):
    if check_permiso(
            db, user_id, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR, a.VER, u.OC
        ):
            lista.append(
                OrdenCargaRemisionResultado(
                    responsable="Gestor de Carga",
                    tarifa_flete=orden_carga.resultado_flete_gestor_carga_tarifa_flete,
                    total_flete=orden_carga.resultado_flete_gestor_carga_total_flete,
                    merma_valor=orden_carga.resultado_flete_gestor_carga_merma_valor,
                    tolerancia=orden_carga.resultado_flete_gestor_carga_merma_tolerancia,
                    tolerancia_kg=orden_carga.resultado_flete_gestor_carga_tolerancia_kg,
                    merma=orden_carga.resultado_flete_gestor_carga_merma,
                    merma_valor_total=(
                        orden_carga.resultado_flete_gestor_carga_merma_valor_total
                    ),
                    merma_valor_total_moneda_local=(
                        orden_carga.resultado_flete_gestor_carga_merma_valor_total_moneda_local
                    ),
                    saldo=orden_carga.resultado_flete_gestor_carga_saldo,
                    complemento_descuento = orden_carga.resultado_gestor_carga_complemento_descuento,

                    # resultado_flete_gestor_carga_saldo (calculo anterior),
                )
            )
    if check_permiso(db, user_id, m.ORDEN_CARGA_REMISION_RESULTADO_PROPIETARIO, a.VER, u.OC):
        lista.append(
            OrdenCargaRemisionResultado(
                responsable="Propietario",
                tarifa_flete=orden_carga.resultado_flete_propietario_tarifa_flete,
                total_flete=orden_carga.resultado_flete_propietario_total_flete,
                merma_valor=orden_carga.resultado_flete_propietario_merma_valor,
                tolerancia=orden_carga.resultado_flete_propietario_merma_tolerancia,
                tolerancia_kg=orden_carga.resultado_flete_propietario_tolerancia_kg,
                merma=orden_carga.resultado_flete_propietario_merma,
                merma_valor_total=orden_carga.resultado_flete_propietario_merma_valor_total,
                merma_valor_total_moneda_local=(
                    orden_carga.resultado_flete_propietario_merma_valor_total_moneda_local
                ),
                total_complemento=orden_carga.resultado_propietario_total_complemento,
                total_descuento=orden_carga.resultado_propietario_total_descuento,
                total_anticipo=orden_carga.resultado_propietario_total_anticipos_retirados,
                saldo=orden_carga.resultado_flete_propietario_saldo,
                complemento_descuento = orden_carga.resultado_propietario_complemento_descuento,
            )
        )
    return lista
