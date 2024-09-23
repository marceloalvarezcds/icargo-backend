from typing import Any, List, Optional, Union

from pydantic import BaseModel

from app.enums import EstadoEnum, OrdenCargaEstadoEnum
from app.enums.tipo_flete import TipoFleteEnum

from .audit_database import AuditDatabase
from .centro_operativo import CentroOperativo
from .date_model import Date
from .flete_anticipo import FleteAnticipo
from .moneda import Moneda
from .movimiento import Movimiento
from .orden_carga_anticipo_porcentaje import (
    OrdenCargaAnticipoPorcentaje,
    OrdenCargaAnticipoPorcentajeForm,
)
from .orden_carga_anticipo_retirado import OrdenCargaAnticipoRetirado
from .orden_carga_anticipo_saldo import OrdenCargaAnticipoSaldo
from .orden_carga_complemento import OrdenCargaComplemento
from .orden_carga_descuento import OrdenCargaDescuento
from .orden_carga_estado_historial import OrdenCargaEstadoHistorial
from .orden_carga_remision_destino import OrdenCargaRemisionDestino
from .orden_carga_remision_origen import OrdenCargaRemisionOrigen
from .orden_carga_remision_resultado import OrdenCargaRemisionResultado
from .rounded_decimal_model import RoundedDecimal


class OrdenCargaForm(BaseModel):
    camion_id: int
    semi_id: int
    flete_id: int
    camion_semi_neto_id: Optional[int] = None
    combinacion_id: Optional[int] = None
    cantidad_nominada: RoundedDecimal
    comentarios: Optional[str] = None
   
    class Config:
        orm_mode = True
        use_enum_values = True    

class OrdenCargaBaseModel(BaseModel):
    camion_id: Optional[int] = None
    semi_id: Optional[int] = None
    flete_id: Optional[int] = None
    cantidad_nominada: Optional[RoundedDecimal] = None
    comentarios: Optional[str] = None
    origen_id: Optional[int] = None
    destino_id: Optional[int] = None
    anticipos_liberados: Optional[bool] = True
    # INICIO Cantidad y Flete
    modify_by_movimiento: Optional[bool] = False
    # inicio - Condiciones para el Gestor de Carga
    condicion_gestor_carga_moneda_id: Optional[int] = None
    condicion_gestor_carga_tarifa: Optional[RoundedDecimal] = None
    # fin - Condiciones para el Gestor de Carga
    # inicio - Condiciones para el Propietario
    condicion_propietario_moneda_id: Optional[int] = None
    condicion_propietario_tarifa: Optional[RoundedDecimal] = None
    # fin - Condiciones para el Propietario
    # FIN Cantidad y Flete
    # INICIO Mermas de Fletes
    # inicio - Mermas para el Gestor de Carga
    merma_gestor_carga_valor: Optional[RoundedDecimal] = None
    merma_gestor_carga_moneda_id: Optional[int] = None
    merma_gestor_carga_es_porcentual: Optional[bool] = False
    merma_gestor_carga_tolerancia: Optional[RoundedDecimal] = None
    # fin - Mermas para el Gestor de Carga
    # inicio - Mermas para el Propietario
    merma_propietario_valor: Optional[RoundedDecimal] = None
    merma_propietario_moneda_id: Optional[int] = None
    merma_propietario_es_porcentual: Optional[bool] = False
    merma_propietario_tolerancia: Optional[RoundedDecimal] = None
    # fin - Mermas para el Propietario
    # FIN Mermas de Fletes


class OrdenCargaEditForm(OrdenCargaBaseModel):
    porcentaje_anticipos: List[OrdenCargaAnticipoPorcentajeForm] = []


class OrdenCarga(OrdenCargaBaseModel):
    id: int
    # Datos de camion
    camion_marca: Optional[str] = None
    combinacion_id: Optional[int] = None
    camion_color: Optional[str] = None
    camion_chofer_nombre: Optional[str] = None
    camion_chofer_numero_documento: Optional[str] = None
    camion_chofer_puede_recibir_anticipos: bool
    camion_limite_cantidad_oc_activas: int
    camion_limite_monto_anticipos: Optional[RoundedDecimal] = None
    camion_monto_anticipo_disponible: Optional[RoundedDecimal] = None
    camion_total_anticipos_retirados_en_estado_pendiente_o_en_proceso: Optional[
        RoundedDecimal
    ] = None
    # Combinacion
    camion_placa: str
    camion_propietario_nombre: str
    camion_propietario_puede_recibir_anticipos: bool
    combinacion_chofer_doc: Optional[str] = None
    camion_beneficiario_nombre: Optional[str] = None
    camion_beneficiario_documento: Optional[str] = None
    camion_propietario_documento: Optional[str] = None
    neto: Optional[int] = None
    # Datos de semi
    semi_placa: str
    semi_marca: Optional[str] = None
    semi_color: Optional[str] = None
    # Datos de fletes
    flete_anticipo_maximo: RoundedDecimal
    flete_destino_id: Optional[int] = None
    flete_destino_nombre: Optional[str] = None
    flete_gestor_carga_id: int
    flete_gestor_carga_nombre: str
    flete_limite_credito: RoundedDecimal
    flete_numero_lote: Optional[str] = None
    flete_monto_efectivo: RoundedDecimal
    flete_monto_efectivo_complemento: RoundedDecimal
    flete_origen_id: Optional[int] = None
    flete_origen_nombre: Optional[str] = None
    flete_producto_descripcion: str
    flete_proyectado: RoundedDecimal
    flete_remitente_nombre: str
    flete_remitente_numero_documento: str
    flete_tarifa: RoundedDecimal
    flete_tipo: Optional[TipoFleteEnum] = None
    flete_saldo: Optional[int] = None
    gestor_carga_id: int
    gestor_carga_nombre: str
    gestor_carga_moneda_nombre: str
    condicion_gestor_cuenta_tarifa: Optional[int] = None
    resultado_gestor_carga_saldo_total: Optional[int] = None
    resultado_propietario_total_anticipos_retirados: Optional[int] = None

    # Historial de Estados
    is_aceptado: bool
    is_cancelado: bool
    is_conciliado: bool
    is_contabilizado: bool
    is_en_proceso: bool
    is_finalizado: bool
    is_liquidado: bool
    # Campos para la edición
    estado: EstadoEnum
    orden_carga_estado: OrdenCargaEstadoEnum
    estado_valor: Union[EstadoEnum, OrdenCargaEstadoEnum]
    anticipos_liberados: bool
    anticipos_liberados_descripcion: str
    # INICIO Tramo de OC
    origen: Optional[CentroOperativo] = None
    destino: Optional[CentroOperativo] = None
    # FIN Tramo de OC
    # INICIO Cantidad y Flete
    # inicio - Condiciones para el Gestor de Carga
    condicion_gestor_carga_moneda: Optional[Moneda] = None
    # fin - Condiciones para el Gestor de Carga
    # inicio - Condiciones para el Propietario
    condicion_propietario_moneda: Optional[Moneda] = None
    # fin - Condiciones para el Propietario
    # FIN Cantidad y Flete
    # INICIO Mermas de Fletes
    # inicio - Mermas para el Gestor de Carga
    merma_gestor_carga_moneda: Optional[Moneda] = None
    merma_gestor_carga_es_porcentual_descripcion: str
    # fin - Mermas para el Gestor de Carga
    # inicio - Mermas para el Propietario
    merma_propietario_moneda: Optional[Moneda] = None
    merma_propietario_es_porcentual_descripcion: str
    # fin - Mermas para el Propietario
    # FIN Mermas de Fletes
    # Relaciones Listas
    auditorias: List[AuditDatabase]
    historial: List[OrdenCargaEstadoHistorial]
    saldos: List[OrdenCargaAnticipoSaldo]
    anticipos: List[OrdenCargaAnticipoRetirado]
    porcentaje_anticipos: List[OrdenCargaAnticipoPorcentaje]
    movimientos: List[Movimiento]
    flete_anticipos: List[FleteAnticipo]
    complementos: List[OrdenCargaComplemento]
    descuentos: List[OrdenCargaDescuento]
    remisiones_destino: List[OrdenCargaRemisionDestino]
    remisiones_origen: List[OrdenCargaRemisionOrigen]
    remisiones_resultado: List[OrdenCargaRemisionResultado]
    remisiones_resultado_flete: List[OrdenCargaRemisionResultado]
    cantidad_destino: RoundedDecimal
    cantidad_origen: RoundedDecimal
    diferencia_origen_destino: RoundedDecimal
    total_anticipo: RoundedDecimal
    total_anticipo_complemento: RoundedDecimal
    total_anticipo_retirado: RoundedDecimal
    total_anticipo_disponible: RoundedDecimal
    resultado_propietario_total_anticipos_retirados_combustible:  Optional[RoundedDecimal] = None
    resultado_propietario_total_anticipos_retirados_efectivo:  Optional[RoundedDecimal] = None
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True

    @classmethod
    def from_orm(cls, obj: Any) -> "OrdenCarga":
        obj.auditorias = []
        obj.remisiones_resultado = []
        obj.remisiones_resultado_flete = []
        return super().from_orm(obj)


class OrdenCargaList(OrdenCargaForm):
    id: int
    # Datos de camion
    camion_chofer_nombre: Optional[str] = None
    camion_chofer_numero_documento: Optional[str] = None
    camion_placa: str
    camion_propietario_nombre: str
    # Datos de semi
    semi_placa: str
    beneficiario_descripcion: Optional[str] = None
    combinacion_id: Optional[int] = None
    # Datos de fletes
    flete_destino_nombre: Optional[str] = None
    flete_gestor_carga_id: int
    flete_gestor_carga_nombre: str
    flete_numero_lote: Optional[str] = None
    flete_origen_nombre: Optional[str] = None
    flete_producto_descripcion: str
    flete_remitente_nombre: str
    flete_remitente_numero_documento: str
    flete_tipo: Optional[TipoFleteEnum] = None
    monto_anticipo_retirado:  Optional[RoundedDecimal] = None
    flete_saldo: Optional[int] = None
    resultado_flete_gestor_carga_merma_valor: Optional[int] = None
    gestor_carga_id: int
    gestor_carga_nombre: str
    gestor_carga_moneda_nombre: str
    condicion_propietario_tarifa: int #Agregar para vista OC
    condicion_gestor_cuenta_tarifa: Optional[int] = None
    # Campos para la edición
    estado: EstadoEnum
    orden_carga_estado: OrdenCargaEstadoEnum
    estado_valor: Union[EstadoEnum, OrdenCargaEstadoEnum]
    anticipos_liberados: bool
    anticipos_liberados_descripcion: str
    # INICIO Tramo de OC
    origen_id: Optional[int] = None
    origen_nombre: Optional[str] = None
    destino_id: Optional[int] = None
    destino_nombre: Optional[str] = None
    # FIN Tramo de OC
    cantidad_destino: RoundedDecimal
    cantidad_origen: RoundedDecimal
    diferencia_origen_destino: RoundedDecimal
    remisiones: str
    nro_tickets: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True

class OrdenCargaBase(BaseModel):
    # Incluye aquí los campos necesarios para mostrar en la respuesta
    id: Optional[int] = None
    combinacion_id: Optional[int] = None

    # Agrega más campos según sea necesario

    class Config:
        orm_mode = True

class OrdenCargaGetList(OrdenCargaBase):
    # Puedes añadir campos adicionales si lo necesitas
    pass

class OrdenCargaUpdateForm(BaseModel):
    comentarios: Optional[str] = None