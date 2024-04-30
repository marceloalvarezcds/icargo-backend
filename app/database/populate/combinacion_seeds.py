# from datetime import date
# from decimal import Decimal
# from random import randrange
# from typing import Optional

# from app.models.camion import Camion
# from app.models.combinacion import Combinacion
# from app.models.producto import Producto
# from app.models.semi import Semi
# from app.repositories.combinacion import get_combinacion_by
# from app.schemas.camion_semi_neto import CamionSemiNeto
# from app.schemas.user import AuthUser
# from sqlalchemy.orm import Session  # type: ignore

# from app.enums import EstadoEnum
# from app.models import (
#     Chofer,
#     Ciudad,
#     Color,
#     GestorCarga,
#     MarcaCamion,
#     MarcaSemi,
#     Pais,
#     Propietario,
#     SemiClasificacion,
#     TipoCamion,
#     TipoCarga,
#     TipoDocumento,
#     TipoPersona,
#     TipoSemi,
#     User,
# )
# from app.repositories import (
#     get_cargo_by_descripcion,
#     get_chofer_by,
#     get_ciudad_by_nombre_and_localidad_id,
#     get_color_by_descripcion,
#     get_contacto_by_email,
#     get_localidad_by_nombre_and_pais_id,
#     get_marca_camion_by_descripcion,
#     get_marca_semi_by_descripcion,
#     get_pais_by_nombre_corto,
#     get_propietario_by,
#     get_semi_clasificacion_by_descripcion,
#     get_tipo_camion_by_descripcion,
#     get_tipo_carga_by_descripcion,
#     get_tipo_documento_by_descripcion,
#     get_tipo_persona_by_descripcion,
#     get_tipo_semi_by_descripcion,
# )
# from app.services import get_user_list_by_gestor_carga_id

# from .camion_seeds import camion_seeds
# from .gestor_carga_propietario_seeds import gestor_carga_propietario_seeds
# from .propietario_contacto_gestor_carga_seeds import (
#     propietario_contacto_gestor_carga_seeds,
# )
# from .semi_seeds import semi_seeds


# def get_chofer_by_tipo_documento_pais_ruc(
#     db: Session,
#     tipo_documento: Optional[TipoDocumento],
#     pais_emisor_documento: Optional[Pais],
#     numero_documento: str,
# ) -> Optional[Chofer]:
#     if tipo_documento and pais_emisor_documento and numero_documento:
#         return get_chofer_by(
#             db, tipo_documento.id, pais_emisor_documento.id, numero_documento
#         )
#     return None


# def combinacion_seeds(
#     db: Session,
#     estado: str,
#     propietario_id: int,
#     chofer_id: int,
#     camion_id: int,
#     semi_id: int,
#     camion: Optional[Camion] = None,
#     semi: Optional[Semi] = None,
#     chofer: Optional[Chofer] = None,
#     propietario: Optional[Propietario] = None,
#     usuario: Optional[AuthUser] = None,
# ):
#     if propietario_id and chofer_id and camion_id and semi_id:
#         obj = get_combinacion_by(db, propietario_id, chofer_id, semi_id)
#         if not obj:
#             combinacion = Combinacion(
#                 estado=estado,
#                 propietario_id=propietario_id,
#                 chofer_id=chofer_id,
#                 camion_id=camion_id,
#                 semi_id=semi_id
#             )
#             db.add(combinacion)
#             db.commit()
#             current_year = date.today().year
#             # Crear registros de camión y semi si no se proporcionan
#             if camion is None:
#                 camion = Camion()
#             if semi is None:
#                 semi = Semi()
#             # Crear registro de camión
#             camion_seeds(
#                 db,
#                 camion=camion,
#                 propietario=propietario,
#                 chofer=chofer,
#                 semi=semi,
#                 usuario=usuario
#             )
#             # Crear registro de semi
#             semi_seeds(
#                 db,
#                 propietario=propietario,
#                 anho=randrange(1990, current_year),
#                 bruto=Decimal(randrange(35000, 50000)),
#                 tara=Decimal(randrange(10000, 30000)),
#             )

#         propietario_objeto = Propietario(nombre="Propietario 1")
#         chofer_objeto = Chofer(nombre="Chofer 1")
#         camion_objeto = Camion(marca="Marca 1")
#         semi_objeto = Semi(placa="Tipo 1")

#         combinacion_seeds(
#             db=db,
#             estado="Activo",  # Estado de la combinación
#             propietario_id=1,  # ID del propietario asociado a la combinación
#             chofer_id=1,  # ID del chofer asociado a la combinación
#             camion_id=1,  # ID del camion asociado a la combinación
#             semi_id=1,  # ID del semi asociado a la combinación
#             propietario= propietario_objeto,
#             semi = semi_objeto,
#             camion = camion_objeto,
#             chofer= chofer_objeto,
#             )