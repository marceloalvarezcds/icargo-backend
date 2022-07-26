from typing import List

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import OrdenCarga, User
from app.schemas import OrdenCargaRemisionResultado
from app.services.permiso import check_permiso


def get_orden_carga_remision_resultado_list_by_orden_carga(
    orden_carga: OrdenCarga, current_user: User
) -> List[OrdenCargaRemisionResultado]:
    lista: List[OrdenCargaRemisionResultado] = []
    if check_permiso(current_user, m.ORDEN_CARGA_REMISION_RESULTADO, a.LISTAR, u.OC):
        if check_permiso(
            current_user, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR, a.VER, u.OC
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
                        orden_carga.resultado_gestor_carga_merma_valor_total_moneda_local
                    ),
                    saldo=orden_carga.resultado_gestor_carga_total_flete,
                    # resultado_gestor_carga_saldo (calculo anterior),
                )
            )
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
                    orden_carga.resultado_propietario_merma_valor_total_moneda_local
                ),
                total_complemento=orden_carga.resultado_propietario_total_complemento,
                total_descuento=orden_carga.resultado_propietario_total_descuento,
                total_anticipo=orden_carga.resultado_propietario_total_anticipos_retirados,
                saldo=orden_carga.resultado_propietario_saldo,
            )
        )
    return lista


def get_orden_carga_remision_resultado_list_by_flete(
    orden_carga: OrdenCarga, current_user: User
) -> List[OrdenCargaRemisionResultado]:
    lista: List[OrdenCargaRemisionResultado] = []
    if check_permiso(current_user, m.ORDEN_CARGA_REMISION_RESULTADO, a.LISTAR, u.OC):
        if check_permiso(
            current_user, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR, a.VER, u.OC
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
                    saldo=orden_carga.resultado_flete_gestor_carga_total_flete,
                    # resultado_flete_gestor_carga_saldo (calculo anterior),
                )
            )
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
            )
        )
    return lista
