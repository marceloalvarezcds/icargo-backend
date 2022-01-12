from enum import Enum


class EstadoEnum(Enum):
    ACTIVO = "Activo"
    ACEPTADO = "Aceptado"
    CANCELADO = "Cancelado"
    CONCILIADO = "Conciliado"
    CONTABILIZADO = "Contabilizado"
    ELIMINADO = "Eliminado"
    EN_PROCESO = "En Proceso"
    FINALIZADO = "Finalizado"
    LIQUIDADO = "Liquidado"
    INACTIVO = "Inactivo"
    NUEVO = "Nuevo"
    PENDIENTE = "Pendiente"
