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
from .gestor_carga_proveedor import GestorCargaProveedor  # noqa
from .gestor_carga_remitente import GestorCargaRemitente  # noqa
from .localidad import Localidad  # noqa
from .moneda import Moneda  # noqa
from .pais import Pais  # noqa
from .proveedor import Proveedor  # noqa
from .proveedor_contacto_gestor_carga import ProveedorContactoGestorCarga  # noqa
from .remitente import Remitente  # noqa
from .remitente_contacto_gestor_carga import RemitenteContactoGestorCarga  # noqa
from .rol import Rol  # noqa
from .tipo_documento import TipoDocumento  # noqa
from .user import User  # noqa
