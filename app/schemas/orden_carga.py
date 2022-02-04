from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel

from app.enums import EstadoEnum, OrdenCargaEstadoEnum
from app.enums.tipo_flete import TipoFleteEnum
from app.schemas.orden_carga_remision_resultado import OrdenCargaRemisionResultado

from .centro_operativo import CentroOperativo
from .date_model import Date
from .flete_anticipo import FleteAnticipo
from .orden_carga_anticipo_retirado import OrdenCargaAnticipoRetirado
from .orden_carga_anticipo_saldo import OrdenCargaAnticipoSaldo
from .orden_carga_complemento import OrdenCargaComplemento
from .orden_carga_descuento import OrdenCargaDescuento
from .orden_carga_remision_destino import OrdenCargaRemisionDestino
from .orden_carga_remision_origen import OrdenCargaRemisionOrigen


class OrdenCargaForm(BaseModel):
    camion_id: int
    semi_id: int
    flete_id: int
    cantidad_nominada: Decimal
    comentarios: Optional[str] = None


class OrdenCargaEditForm(BaseModel):
    camion_id: Optional[int] = None
    semi_id: Optional[int] = None
    flete_id: Optional[int] = None
    cantidad_nominada: Optional[Decimal] = None
    comentarios: Optional[str] = None
    origen_id: Optional[int] = None
    destino_id: Optional[int] = None


class OrdenCarga(OrdenCargaForm):
    id: int
    # Datos de camion
    camion_chofer_nombre: str
    camion_chofer_numero_documento: str
    camion_placa: str
    camion_propietario_nombre: str
    # Datos de semi
    semi_placa: str
    # Datos de fletes
    flete_anticipo_maximo: Decimal
    flete_destino_id: int
    flete_destino_nombre: str
    flete_gestor_carga_id: int
    flete_gestor_carga_nombre: str
    flete_limite_credito: Decimal
    flete_numero_lote: str
    flete_monto_efectivo: Decimal
    flete_origen_id: int
    flete_origen_nombre: str
    flete_producto_descripcion: str
    flete_proyectado: Decimal
    flete_remitente_nombre: str
    flete_remitente_numero_documento: str
    flete_tarifa: Decimal
    flete_tipo: TipoFleteEnum
    gestor_carga_id: int
    gestor_carga_nombre: str
    gestor_carga_moneda_nombre: str
    # Campos para la edición
    estado: EstadoEnum
    orden_carga_estado: OrdenCargaEstadoEnum
    estado_valor: Union[EstadoEnum, OrdenCargaEstadoEnum]
    anticipos_liberados: bool
    anticipos_liberados_descripcion: str
    # INICIO Tramo de OC
    origen_id: int
    origen: CentroOperativo
    destino_id: int
    destino: CentroOperativo
    # FIN Tramo de OC
    # Historial de estados
    fecha_aceptado: Optional[Date] = None
    fecha_cancelado: Optional[Date] = None
    fecha_conciliado: Optional[Date] = None
    fecha_contabilizado: Optional[Date] = None
    fecha_en_proceso: Optional[Date] = None
    fecha_finalizado: Optional[Date] = None
    fecha_liquidado: Optional[Date] = None
    fecha_nuevo: Optional[Date] = None
    fecha_pendiente: Optional[Date] = None
    # Historial de estados de OC
    fecha_arribado_a_cargar: Optional[Date] = None
    fecha_arribado_a_descargar: Optional[Date] = None
    fecha_cargado: Optional[Date] = None
    fecha_descargado: Optional[Date] = None
    # Relaciones Listas
    saldos: List[OrdenCargaAnticipoSaldo]
    anticipos: List[OrdenCargaAnticipoRetirado]
    flete_anticipos: List[FleteAnticipo]
    complementos: List[OrdenCargaComplemento]
    descuentos: List[OrdenCargaDescuento]
    remisiones_destino: List[OrdenCargaRemisionDestino]
    remisiones_origen: List[OrdenCargaRemisionOrigen]
    remisiones_resultado: List[OrdenCargaRemisionResultado]
    cantidad_destino: Decimal
    cantidad_origen: Decimal
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True


class OrdenCargaList(OrdenCargaForm):
    id: int
    # Datos de camion
    camion_chofer_nombre: str
    camion_chofer_numero_documento: str
    camion_placa: str
    camion_propietario_nombre: str
    # Datos de semi
    semi_placa: str
    # Datos de fletes
    flete_destino_nombre: str
    flete_gestor_carga_id: int
    flete_gestor_carga_nombre: str
    flete_numero_lote: str
    flete_origen_nombre: str
    flete_producto_descripcion: str
    flete_remitente_nombre: str
    flete_remitente_numero_documento: str
    flete_tipo: TipoFleteEnum
    gestor_carga_id: int
    gestor_carga_nombre: str
    gestor_carga_moneda_nombre: str
    # Campos para la edición
    estado: EstadoEnum
    orden_carga_estado: OrdenCargaEstadoEnum
    estado_valor: Union[EstadoEnum, OrdenCargaEstadoEnum]
    anticipos_liberados: bool
    anticipos_liberados_descripcion: str
    # INICIO Tramo de OC
    origen_id: int
    origen_nombre: str
    destino_id: int
    destino_nombre: str
    # FIN Tramo de OC
    cantidad_destino: Decimal
    cantidad_origen: Decimal
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
