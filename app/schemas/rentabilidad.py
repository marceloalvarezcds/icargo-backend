from typing import Any, List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum, TipoFleteEnum

from .date_model import Date
from .rounded_decimal_model import RoundedDecimal


class Rentabilidad(BaseModel):
    estado: EstadoEnum
    oc_id: int
    flete_id: int
    nro_remisiones: str
    estado_anticipo: str
    chofer_nombre: Optional[str] = None
    chofer_tipo_documento: Optional[str] = None
    chofer_numero_documento: Optional[str] = None
    camion_placa: str
    semi_placa: str
    propietario_nombre: str
    flete_tipo: Optional[TipoFleteEnum] = None
    producto_descripcion: str
    cantidad_nominada: RoundedDecimal
    cantidad_destino: RoundedDecimal
    cantidad_origen: RoundedDecimal
    diferencia_origen_destino: RoundedDecimal
    remitente_nombre: str
    gestor_carga_pais_id: Optional[int] = None
    origen_nombre: str
    origen_pais_id: Optional[int] = None
    destino_nombre: str
    destino_pais_id: Optional[int] = None
    lugar_carga_nombre: str
    lugar_descarga_nombre: str
    # PAGO FLETE a PROPIETARIO p/GC
    condicion_propietario_tarifa: RoundedDecimal
    condicion_propietario_moneda_nombre: str
    condicion_propietario_moneda_simbolo: str
    condicion_propietario_unidad_descripcion: str
    condicion_propietario_unidad_abreviatura: str
    propietario_flete_total: RoundedDecimal  # cantidad_destino * tarifa
    propietario_flete_total_ml: RoundedDecimal  # cantidad_destino * tarifa (Moneda Local)
    flete_condicion_propietario_tarifa: RoundedDecimal
    flete_condicion_propietario_moneda_nombre: str
    flete_condicion_propietario_moneda_simbolo: str
    flete_propietario_total: RoundedDecimal  # cantidad_destino * flete_tarifa
    flete_propietario_total_ml: RoundedDecimal  # cantidad_destino * flete_tarifa (Moneda Local)
    # COBRO por MERMA a PROPIETARIO p/GC
    merma_propietario_valor: RoundedDecimal
    merma_propietario_moneda_nombre: str
    merma_propietario_moneda_simbolo: str
    merma_propietario_unidad_descripcion: str
    merma_propietario_unidad_abreviatura: str
    merma_propietario_es_porcentual: bool
    merma_propietario_tolerancia_original: RoundedDecimal
    merma_propietario_tolerancia: RoundedDecimal  # Si es_porcentual entonces (cantidad_origen * tolerancia_original) sino tolerancia_original # noqa
    merma_propietario_merma: RoundedDecimal  # Si (diferencia_origen_destino - tolerancia) > 0 entonces (diferencia_origen_destino - tolerancia) sino 0 # noqa
    merma_propietario_valor_merma: RoundedDecimal  # valor * merma
    flete_merma_propietario_valor: RoundedDecimal
    flete_merma_propietario_moneda_nombre: str
    flete_merma_propietario_moneda_simbolo: str
    flete_merma_propietario_es_porcentual: bool
    flete_merma_propietario_tolerancia_original: RoundedDecimal
    flete_merma_propietario_tolerancia: RoundedDecimal  # Si es_porcentual entonces (cantidad_origen * tolerancia_original) sino tolerancia_original # noqa
    flete_merma_propietario_merma: RoundedDecimal  # Si (diferencia_origen_destino - tolerancia) > 0 entonces (diferencia_origen_destino - tolerancia) sino 0 # noqa
    flete_merma_propietario_valor_merma: RoundedDecimal  # flete_valor * merma
    # COBRO FLETE a REMITENTE p/GC
    condicion_gestor_carga_tarifa: RoundedDecimal
    condicion_gestor_carga_moneda_nombre: str
    condicion_gestor_carga_moneda_simbolo: str
    condicion_gestor_carga_unidad_descripcion: str
    condicion_gestor_carga_unidad_abreviatura: str
    gestor_carga_flete_total: RoundedDecimal  # cantidad_destino * tarifa
    gestor_carga_flete_total_ml: RoundedDecimal  # cantidad_destino * tarifa (Moneda Local)
    flete_condicion_gestor_carga_moneda_nombre: str
    flete_condicion_gestor_carga_moneda_simbolo: str
    flete_condicion_gestor_carga_tarifa: RoundedDecimal
    flete_gestor_carga_total: RoundedDecimal  # cantidad_destino * flete_tarifa
    flete_gestor_carga_total_ml: RoundedDecimal  # cantidad_destino * flete_tarifa (Moneda Local)  # noqa: B950
    # PAGO por MERMA a REMITENTE p/GC
    merma_gestor_carga_valor: RoundedDecimal
    merma_gestor_carga_moneda_nombre: str
    merma_gestor_carga_moneda_simbolo: str
    merma_gestor_carga_unidad_descripcion: str
    merma_gestor_carga_unidad_abreviatura: str
    merma_gestor_carga_es_porcentual: bool
    merma_gestor_carga_tolerancia_original: RoundedDecimal
    merma_gestor_carga_tolerancia: RoundedDecimal  # Si es_porcentual entonces (cantidad_origen * tolerancia_original) sino tolerancia_original # noqa
    merma_gestor_carga_merma: RoundedDecimal  # Si (diferencia_origen_destino - tolerancia) > 0 entonces (diferencia_origen_destino - tolerancia) sino 0 # noqa
    merma_gestor_carga_valor_merma: RoundedDecimal  # valor * merma
    flete_merma_gestor_carga_valor: RoundedDecimal
    flete_merma_gestor_carga_moneda_nombre: str
    flete_merma_gestor_carga_moneda_simbolo: str
    flete_merma_gestor_carga_es_porcentual: bool
    flete_merma_gestor_carga_tolerancia_original: RoundedDecimal
    flete_merma_gestor_carga_tolerancia: RoundedDecimal  # Si es_porcentual entonces (cantidad_origen * tolerancia_original) sino tolerancia_original # noqa
    flete_merma_gestor_carga_merma: RoundedDecimal  # Si (diferencia_origen_destino - tolerancia) > 0 entonces (diferencia_origen_destino - tolerancia) sino 0 # noqa
    flete_merma_gestor_carga_valor_merma: RoundedDecimal  # flete_valor * merma
    # Complementos
    total_complemento_a_pagar: RoundedDecimal
    total_complemento_a_cobrar: RoundedDecimal
    diferencia_complemento: RoundedDecimal
    # Descuentos
    total_descuento_a_pagar: RoundedDecimal
    total_descuento_a_cobrar: RoundedDecimal
    diferencia_descuento: RoundedDecimal
    # RESULTADOS
    total_anticipo_retirado: RoundedDecimal
    saldo_gestor_carga: RoundedDecimal
    saldo_propietario: RoundedDecimal
    # Auditoría
    fecha_conciliacion: Optional[Date]
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True

    @classmethod
    def get_by_oc(cls, item: Any) -> "Rentabilidad":
        return Rentabilidad(
            estado=item.estado,
            oc_id=item.id,
            flete_id=item.flete_id,
            nro_remisiones=item.remisiones,
            estado_anticipo="Liberados" if item.anticipos_liberados else "Bloqueados",
            chofer_nombre=item.camion_chofer_nombre,
            chofer_tipo_documento=item.camion.chofer.tipo_documento.descripcion
            if item.camion.chofer
            else None,
            chofer_numero_documento=item.camion_chofer_numero_documento,
            camion_placa=item.camion_placa,
            semi_placa=item.semi_placa,
            propietario_nombre=item.camion_propietario_nombre,
            flete_tipo=item.flete_tipo,
            producto_descripcion=item.flete_producto_descripcion,
            cantidad_nominada=item.cantidad_nominada,
            cantidad_destino=item.cantidad_destino,
            cantidad_origen=item.cantidad_origen,
            diferencia_origen_destino=item.diferencia_origen_destino,
            remitente_nombre=item.flete_remitente_nombre,
            gestor_carga_pais_id=item.gestor_carga.pais_id,
            origen_nombre=item.flete_origen_nombre,
            origen_pais_id=item.flete.origen.pais_id,
            destino_nombre=item.flete_destino_nombre,
            destino_pais_id=item.flete.destino.pais_id,
            lugar_carga_nombre=item.origen_nombre,
            lugar_descarga_nombre=item.destino_nombre,
            # PAGO FLETE a PROPIETARIO p/GC
            condicion_propietario_tarifa=item.condicion_propietario_tarifa,
            condicion_propietario_moneda_nombre=item.condicion_propietario_moneda.nombre,
            condicion_propietario_moneda_simbolo=item.condicion_propietario_moneda.simbolo,  # noqa: B950
            condicion_propietario_unidad_descripcion=item.flete.condicion_propietario_unidad.descripcion,  # noqa: B950
            condicion_propietario_unidad_abreviatura=item.flete.condicion_propietario_unidad.abreviatura,  # noqa: B950
            propietario_flete_total=item.resultado_propietario_total_flete,
            propietario_flete_total_ml=item.resultado_propietario_total_flete,
            flete_condicion_propietario_tarifa=item.flete_tarifa,
            flete_condicion_propietario_moneda_nombre=item.flete.condicion_propietario_moneda.nombre,  # noqa: B950
            flete_condicion_propietario_moneda_simbolo=item.flete.condicion_propietario_moneda.simbolo,  # noqa: B950
            flete_propietario_total=item.resultado_flete_propietario_total_flete,
            flete_propietario_total_ml=item.resultado_flete_propietario_total_flete,
            # COBRO por MERMA a PROPIETARIO p/GC
            merma_propietario_valor=item.merma_propietario_valor,
            merma_propietario_moneda_nombre=item.flete.merma_propietario_moneda.nombre,
            merma_propietario_moneda_simbolo=item.flete.merma_propietario_moneda.simbolo,
            merma_propietario_unidad_descripcion=item.flete.merma_propietario_unidad.descripcion,  # noqa: B950
            merma_propietario_unidad_abreviatura=item.flete.merma_propietario_unidad.abreviatura,  # noqa: B950
            merma_propietario_es_porcentual=item.flete.merma_propietario_es_porcentual,
            merma_propietario_tolerancia_original=item.merma_propietario_tolerancia,
            merma_propietario_tolerancia=item.resultado_propietario_tolerancia_kg,
            merma_propietario_merma=item.resultado_propietario_merma,
            merma_propietario_valor_merma=item.resultado_propietario_merma_valor_total,
            flete_merma_propietario_valor=item.flete.merma_propietario_valor,
            flete_merma_propietario_moneda_nombre=item.flete.merma_propietario_moneda.nombre,
            flete_merma_propietario_moneda_simbolo=item.flete.merma_propietario_moneda.simbolo,
            flete_merma_propietario_es_porcentual=item.flete.merma_propietario_es_porcentual,
            flete_merma_propietario_tolerancia_original=item.flete.merma_propietario_tolerancia,  # noqa: B950
            flete_merma_propietario_tolerancia=item.resultado_flete_propietario_tolerancia_kg,
            flete_merma_propietario_merma=item.resultado_flete_propietario_merma,
            flete_merma_propietario_valor_merma=item.resultado_flete_propietario_merma_valor_total,  # noqa: B950
            # COBRO FLETE a REMITENTE p/GC
            condicion_gestor_carga_tarifa=item.condicion_gestor_carga_tarifa,
            condicion_gestor_carga_moneda_nombre=item.condicion_gestor_carga_moneda.nombre,  # noqa: B950
            condicion_gestor_carga_moneda_simbolo=item.condicion_gestor_carga_moneda.simbolo,  # noqa: B950
            condicion_gestor_carga_unidad_descripcion=item.flete.condicion_gestor_cuenta_unidad.descripcion,  # noqa: B950
            condicion_gestor_carga_unidad_abreviatura=item.flete.condicion_gestor_cuenta_unidad.abreviatura,  # noqa: B950
            gestor_carga_flete_total=item.resultado_gestor_carga_total_flete,
            gestor_carga_flete_total_ml=item.resultado_gestor_carga_total_flete,
            flete_condicion_gestor_carga_tarifa=item.flete_tarifa_gestor_carga,
            flete_condicion_gestor_carga_moneda_nombre=item.condicion_gestor_carga_moneda.nombre,  # noqa: B950
            flete_condicion_gestor_carga_moneda_simbolo=item.condicion_gestor_carga_moneda.simbolo,  # noqa: B950
            flete_gestor_carga_total=item.resultado_flete_gestor_carga_total_flete,
            flete_gestor_carga_total_ml=item.resultado_flete_gestor_carga_total_flete,
            # PAGO por MERMA a REMITENTE p/GC
            merma_gestor_carga_valor=item.merma_gestor_carga_valor,
            merma_gestor_carga_moneda_nombre=item.merma_gestor_carga_moneda.nombre,
            merma_gestor_carga_moneda_simbolo=item.merma_gestor_carga_moneda.simbolo,
            merma_gestor_carga_unidad_descripcion=item.flete.merma_gestor_cuenta_unidad.descripcion,  # noqa: B950
            merma_gestor_carga_unidad_abreviatura=item.flete.merma_gestor_cuenta_unidad.abreviatura,  # noqa: B950
            merma_gestor_carga_es_porcentual=item.merma_gestor_carga_es_porcentual,
            merma_gestor_carga_tolerancia_original=item.merma_gestor_carga_tolerancia,
            merma_gestor_carga_tolerancia=item.resultado_gestor_carga_tolerancia_kg,
            merma_gestor_carga_merma=item.resultado_gestor_carga_merma,
            merma_gestor_carga_valor_merma=item.resultado_gestor_carga_merma_valor_total,
            flete_merma_gestor_carga_valor=item.flete.merma_gestor_cuenta_valor,
            flete_merma_gestor_carga_moneda_nombre=item.flete.merma_gestor_cuenta_moneda.nombre,
            flete_merma_gestor_carga_moneda_simbolo=item.flete.merma_gestor_cuenta_moneda.simbolo,  # noqa: B950
            flete_merma_gestor_carga_es_porcentual=item.flete.merma_gestor_cuenta_es_porcentual,
            flete_merma_gestor_carga_tolerancia_original=item.flete.merma_gestor_carga_tolerancia,  # noqa: B950
            flete_merma_gestor_carga_tolerancia=item.resultado_flete_gestor_carga_tolerancia_kg,
            flete_merma_gestor_carga_merma=item.resultado_flete_gestor_carga_merma,
            flete_merma_gestor_carga_valor_merma=item.resultado_flete_gestor_carga_merma_valor_total,  # noqa: B950
            # Complementos
            total_complemento_a_pagar=item.resultado_propietario_total_complemento,
            total_complemento_a_cobrar=item.resultado_propietario_total_complemento_a_cobrar,
            diferencia_complemento=item.resultado_diferencia_complemento,
            # Descuentos
            total_descuento_a_pagar=item.resultado_propietario_total_descuento_a_pagar,
            total_descuento_a_cobrar=item.resultado_propietario_total_descuento,
            diferencia_descuento=item.resultado_diferencia_descuento,
            # RESULTADOS
            total_anticipo_retirado=item.resultado_propietario_total_anticipos_retirados,
            saldo_gestor_carga=item.resultado_gestor_carga_saldo_total,
            saldo_propietario=item.resultado_propietario_saldo_total,
            # Auditoría
            fecha_conciliacion=item.fecha_conciliacion,
            created_by=item.created_by,
            created_at=item.created_at,
            modified_by=item.modified_by,
            modified_at=item.modified_at,
        )

    @classmethod
    def get_list_by_oc(cls, list: List[Any]) -> List["Rentabilidad"]:
        return [cls.get_by_oc(it) for it in list]
