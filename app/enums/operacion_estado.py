from enum import Enum


class OperacionEstadoEnum(Enum):
    EMITIDO = "Emitido"
    CONFIRMADO = "Confirmado"
    RECHAZADO = "Rechazado"
