from enum import Enum


class OrdenCargaEstadoEnum(Enum):
    PENDIENTE = "Pendiente"
    ARRIBADO_A_CARGAR = "Arribado a cargar"
    ARRIBADO_A_DESCARGAR = "Arribado a descargar"
    CARGADO = "Cargado"
    DESCARGADO = "Descargado"
