from typing import List

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import OrdenCarga, User
from app.schemas import OrdenCargaRemisionResultado
from app.services.permiso import check_permiso


def get_orden_carga_remision_resultado_list_by_orden_carga(
    orden_carga: OrdenCarga, current_user: User
) -> List[OrdenCargaRemisionResultado]:
    lista: List[OrdenCargaRemisionResultado] = []
    if check_permiso(current_user, m.ORDEN_CARGA_REMISION_RESULTADO, a.LISTAR):
        if check_permiso(current_user, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR, a.VER):
            lista.append(
                OrdenCargaRemisionResultado(
                    responsable="Gestor de Cuenta",
                    tarifa_flete=orden_carga.resultado_gestor_carga_tarifa_flete,
                    total_flete=orden_carga.resultado_gestor_carga_total_flete,
                    merma_valor=orden_carga.resultado_gestor_carga_merma_valor,
                    tolerancia=orden_carga.resultado_gestor_carga_merma_tolerancia,
                    tolerancia_kg=orden_carga.resultado_gestor_carga_tolerancia_kg,
                    merma=orden_carga.resultado_gestor_carga_merma,
                    merma_valor_total=orden_carga.resultado_gestor_carga_merma_valor_total,
                    merma_valor_total_moneda_local=(
                        orden_carga.resultado_gestor_carga_merma_valor_total_moneda_local
                    ),
                    saldo=orden_carga.resultado_gestor_carga_saldo,
                )
            )
        lista.append(
            OrdenCargaRemisionResultado(
                responsable="Propietario",
                tarifa_flete=orden_carga.resultado_propietario_tarifa_flete,
                total_flete=orden_carga.resultado_propietario_total_flete,
                merma_valor=orden_carga.resultado_propietario_merma_valor,
                tolerancia=orden_carga.resultado_propietario_merma_tolerancia,
                tolerancia_kg=orden_carga.resultado_propietario_tolerancia_kg,
                merma=orden_carga.resultado_propietario_merma,
                merma_valor_total=orden_carga.resultado_propietario_merma_valor_total,
                merma_valor_total_moneda_local=(
                    orden_carga.resultado_propietario_merma_valor_total_moneda_local
                ),
                total_complemento=orden_carga.resultado_propietario_total_complemento,
                total_descuento=orden_carga.resultado_propietario_total_descuento,
                total_anticipo=orden_carga.flete_limite_credito,
                saldo=orden_carga.resultado_propietario_saldo,
            )
        )
    return lista
