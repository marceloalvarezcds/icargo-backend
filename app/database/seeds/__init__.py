from sqlalchemy.orm import Session  # type: ignore

from .centro_operativo_clasificacion_seeds import centro_operativo_clasificacion_seeds
from .color_seeds import color_seeds
from .ente_emisor_automotor_seeds import ente_emisor_automotor_seeds
from .ente_emisor_transporte_seeds import ente_emisor_transporte_seeds
from .marca_camion_seeds import marca_camion_seeds
from .marca_semi_seeds import marca_semi_seeds
from .moneda_seeds import moneda_seeds
from .pais_seeds import pais_seeds
from .producto_seeds import producto_seeds
from .rol_seeds import rol_seeds
from .semi_clasificacion_seeds import semi_clasificacion_seeds
from .tipo_anticipo_seeds import tipo_anticipo_seeds
from .tipo_camion_seeds import tipo_camion_seeds
from .tipo_carga_seeds import tipo_carga_seeds
from .tipo_concepto_complemento_seeds import tipo_concepto_complemento_seeds
from .tipo_concepto_descuento_seeds import tipo_concepto_descuento_seeds
from .tipo_persona_seeds import tipo_persona_seeds
from .tipo_registro_seeds import tipo_registro_seeds
from .tipo_semi_seeds import tipo_semi_seeds
from .unidad_seeds import unidad_seeds
from .user_seeds import user_seeds


def seeds(db: Session):
    centro_operativo_clasificacion_seeds(db)
    color_seeds(db)
    ente_emisor_transporte_seeds(db)
    marca_camion_seeds(db)
    marca_semi_seeds(db)
    moneda_seeds(db)
    pais_seeds(db)
    producto_seeds(db)
    rol_seeds(db)
    semi_clasificacion_seeds(db)
    tipo_anticipo_seeds(db)
    tipo_camion_seeds(db)
    tipo_carga_seeds(db)
    tipo_concepto_complemento_seeds(db)
    tipo_concepto_descuento_seeds(db)
    tipo_persona_seeds(db)
    tipo_registro_seeds(db)
    tipo_semi_seeds(db)
    unidad_seeds(db)
    user_seeds(db)
    ente_emisor_automotor_seeds(db)
