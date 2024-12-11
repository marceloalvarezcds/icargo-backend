from enum import Enum


class MovimientoEstadoEnum(Enum):
    PROVISION = "Provision"
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    CONFIRMADO = "Confirmado"
    FINALIZADO = "Finalizado"
    ELIMINADO = "Eliminado"
