# should be imported to help code editor (vscode) for autocompletion
from .cargo import get_cargo_by_descripcion, get_cargo_list  # noqa
from .centro_operativo import (  # noqa
    create_centro_operativo,
    edit_centro_operativo,
    get_centro_operativo_by_id,
    get_centro_operativo_list,
)
from .centro_operativo_clasificacion import (  # noqa
    get_centro_operativo_clasificacion_by_nombre,
    get_centro_operativo_clasificacion_list,
)
from .centro_operativo_contacto_gestor_carga import (  # noqa
    create_centro_operativo_contacto_gestor_carga,
    delete_centro_operativo_contacto_gestor_carga,
    edit_centro_operativo_contacto_gestor_carga,
    get_centro_operativo_contacto_gestor_carga_by,
)
from .ciudad import get_ciudad_by_nombre_and_localidad_id, get_ciudad_list  # noqa
from .composicion_juridica import get_composicion_juridica_by_nombre  # noqa
from .contacto import (  # noqa
    create_contacto,
    edit_contacto,
    get_contacto_by_email,
    get_contacto_by_id,
    get_contacto_by_telefono,
    get_contacto_by_telefono_and_email,
)
from .localidad import get_localidad_by_nombre_and_pais_id, get_localidad_list  # noqa
from .moneda import get_moneda_by_simbolo  # noqa
from .pais import get_pais_by_nombre_corto, get_pais_list  # noqa
from .rol import get_rol_by_codigo, get_rol_list  # noqa
from .tipo_documento import get_tipo_documento_by_descripcion  # noqa
from .user import create, get, get_by_email, get_by_username  # noqa
