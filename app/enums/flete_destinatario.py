from enum import Enum


class FleteDestinatarioEnum(Enum):
    CENTRO_OPERATIVO = "centro_operativo"
    REMITENTE = "Remitente"
    USUARIO = "Usuario"


class FleteDestinatarioCentroOperativoEnum(Enum):
    ORIGEN = "Origen"
    DESTINO = "Destino"
