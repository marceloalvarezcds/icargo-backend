from enum import Enum


class LiquidacionEtapaEnum(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    CONFIRMADO = "Confirmado"
    PAGOS = 'Pagos/Cobros'
    FINALIZADO = "Finalizado"
