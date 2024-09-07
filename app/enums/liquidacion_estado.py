from enum import Enum


class LiquidacionEstadoEnum(Enum):
    ACEPTADO = "Aceptado"
    CANCELADO = "Cancelado"
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    NUEVO = "Nuevo"
    EN_REVISION = "En Revisión"
    CONFIRMADO = "Confirmado"
    FINALIZADO = "Finalizado"
    RECHAZADO = "Rechazado"
    SALDO_ABIERTO = "Saldo abierto"
    SALDO_CERRADO = "Saldo cerrado"
    ELIMINADO = "Eliminado"
