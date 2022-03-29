from enum import Enum


class MovimientoEstadoEnum(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    CONFIRMADO = "Confirmado"
    FINALIZADO = "Finalizado"
    ELIMINADO = "Eliminado"
