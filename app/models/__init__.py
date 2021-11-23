# debe importarse para que alembic pueda detectar y crear las tablas
from app import audits  # noqa
from app.database import Base  # noqa

from .cargo import Cargo  # noqa
from .centro_operativo import CentroOperativo  # noqa
from .centro_operativo_clasificacion import CentroOperativoClasificacion  # noqa
from .centro_operativo_contacto_gestor_carga import (  # noqa
    CentroOperativoContactoGestorCarga,
)
from .ciudad import Ciudad  # noqa
from .composicion_juridica import ComposicionJuridica  # noqa
from .contacto import Contacto  # noqa
from .gestor_carga import GestorCarga  # noqa
from .gestor_carga_centro_operativo import GestorCargaCentroOperativo  # noqa
from .gestor_carga_propietario import GestorCargaPropietario  # noqa
from .gestor_carga_proveedor import GestorCargaProveedor  # noqa
from .gestor_carga_punto_venta import GestorCargaPuntoVenta  # noqa
from .gestor_carga_remitente import GestorCargaRemitente  # noqa
from .localidad import Localidad  # noqa
from .moneda import Moneda  # noqa
from .pais import Pais  # noqa
from .permiso import Permiso  # noqa
from .propietario import Propietario  # noqa
from .propietario_contacto_gestor_carga import PropietarioContactoGestorCarga  # noqa
from .proveedor import Proveedor  # noqa
from .proveedor_contacto_gestor_carga import ProveedorContactoGestorCarga  # noqa
from .punto_venta import PuntoVenta  # noqa
from .punto_venta_contacto_gestor_carga import PuntoVentaContactoGestorCarga  # noqa
from .remitente import Remitente  # noqa
from .remitente_contacto_gestor_carga import RemitenteContactoGestorCarga  # noqa
from .rol import Rol  # noqa
from .tipo_documento import TipoDocumento  # noqa
from .tipo_persona import TipoPersona  # noqa
from .tipo_registro import TipoRegistro  # noqa
from .user import User  # noqa
