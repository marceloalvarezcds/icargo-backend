from enum import Enum


class LiquidacionEtapaEnum(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    CONFIRMADO = "Confirmado"
    FINALIZADO = "Finalizado"
