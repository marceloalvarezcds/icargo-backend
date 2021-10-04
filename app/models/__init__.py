# debe importarse para que alembic pueda detectar y crear las tablas
from app import audits  # noqa
from app.database import Base  # noqa

from .centro_operativo import CentroOperativo  # noqa
from .centro_operativo_clasificacion import CentroOperativoClasificacion  # noqa
from .ciudad import Ciudad  # noqa
from .contacto import Contacto  # noqa
from .localidad import Localidad  # noqa
from .pais import Pais  # noqa
from .user import User  # noqa
