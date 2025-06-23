from decimal import Decimal
from typing import Any

from .number import number_format


def get_tarifa_unidad(moneda: Any, unidad: Any):
    return f"{moneda.simbolo}/{unidad.abreviatura}"  # noqa


def get_flete_detalle(oc: Any, tarifa: Decimal, moneda: Any, unidad: Any):
    remi = f"{oc.flete.remitente_nombre} ||"
    dest = f"P.Dest.: {number_format(oc.cantidad_destino)}Kg ||"
    tari = (
        f"{number_format(tarifa)}{get_tarifa_unidad(moneda, unidad)} ||"  # noqa: B950
    )
    nums = f"Nº Rem: {oc.remisiones} || Tickets: {oc.nro_tickets} ||"
    ubic = f"Ori: {oc.origen_nombre} || Des: {oc.destino_nombre}"
    return f"{remi} {dest} {tari} {nums} {ubic}"


def get_merma_tolerancia_kg(
    tolerancia: Decimal, es_porcentual: bool, conversion_kg: Decimal
):
    return tolerancia if es_porcentual else tolerancia * conversion_kg


def get_resultado_tolerancia_kg(
    cantidad_origen: Decimal,
    tolerancia: Decimal,
    es_porcentual: bool,
    conversion_kg: Decimal,
):
    return (
        (tolerancia / Decimal(100)) * cantidad_origen
        if es_porcentual
        else get_merma_tolerancia_kg(tolerancia, es_porcentual, conversion_kg)
    )


def get_resultado_merma(diferencia_origen_destino: Decimal, tolerancia_kg: Decimal):
    return (
        (diferencia_origen_destino - tolerancia_kg)
        if (diferencia_origen_destino - tolerancia_kg) > 0
        else 0
    )


def get_merma_detalle(
    oc: Any,
    valor: Decimal,
    tolerancia: Decimal,
    es_porcentual: bool,
    moneda: Any,
    unidad: Any,
):
    tolerancia_kg = get_resultado_tolerancia_kg(
        oc.cantidad_origen, tolerancia, es_porcentual, unidad.conversion_kg
    )
    resultado_merma = get_resultado_merma(oc.diferencia_origen_destino, tolerancia_kg)
    remi = f"{oc.flete.remitente_nombre} ||"
    diff = f"Dif.: {number_format(oc.diferencia_origen_destino)}Kg ||"
    totl = f"Tol.: {number_format(tolerancia_kg)}Kg ||"
    merm = f"M.: {number_format(resultado_merma)}Kg ||"
    mval = f"{number_format(valor)}{get_tarifa_unidad(moneda, unidad)} ||"
    nums = f"Nº Rem: {oc.remisiones} || Tickets: {oc.nro_tickets} ||"
    ubic = f"Ori: {oc.origen_nombre} || Des: {oc.destino_nombre}"
    return f"{remi} {diff} {totl} {merm} {mval} {nums} {ubic}"
