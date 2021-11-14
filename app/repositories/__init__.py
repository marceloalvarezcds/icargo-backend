# should be imported to help code editor (vscode) for autocompletion
from .cargo import get_cargo_by_descripcion, get_cargo_list  # noqa
from .centro_operativo import (  # noqa
    create_centro_operativo,
    delete_centro_operativo,
    edit_centro_operativo,
    get_centro_operativo_by,
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
from .composicion_juridica import (  # noqa
    get_composicion_juridica_by_nombre,
    get_composicion_juridica_list,
)
from .contacto import (  # noqa
    create_contacto,
    edit_contacto,
    get_contacto_by_email,
    get_contacto_by_id,
    get_contacto_by_telefono,
    get_contacto_by_telefono_and_email,
)
from .gestor_carga import (  # noqa
    create_gestor_carga,
    delete_gestor_carga,
    edit_gestor_carga,
    get_gestor_carga_by,
    get_gestor_carga_by_id,
    get_gestor_carga_list,
)
from .gestor_carga_centro_operativo import (  # noqa
    create_gestor_carga_centro_operativo,
    edit_gestor_carga_centro_operativo,
    get_gestor_carga_centro_operativo_by,
)
from .gestor_carga_proveedor import (  # noqa
    create_gestor_carga_proveedor,
    edit_gestor_carga_proveedor,
    get_gestor_carga_proveedor_by,
)
from .gestor_carga_punto_venta import (  # noqa
    create_gestor_carga_punto_venta,
    edit_gestor_carga_punto_venta,
    get_gestor_carga_punto_venta_by,
)
from .gestor_carga_remitente import (  # noqa
    create_gestor_carga_remitente,
    edit_gestor_carga_remitente,
    get_gestor_carga_remitente_by,
)
from .localidad import get_localidad_by_nombre_and_pais_id, get_localidad_list  # noqa
from .moneda import get_moneda_by_simbolo, get_moneda_list  # noqa
from .pais import get_pais_by_nombre_corto, get_pais_list  # noqa
from .permiso import get_permiso_by, get_permiso_list  # noqa
from .proveedor import (  # noqa
    create_proveedor,
    delete_proveedor,
    edit_proveedor,
    get_proveedor_by,
    get_proveedor_by_id,
    get_proveedor_list,
)
from .proveedor_contacto_gestor_carga import (  # noqa
    create_proveedor_contacto_gestor_carga,
    delete_proveedor_contacto_gestor_carga,
    edit_proveedor_contacto_gestor_carga,
    get_proveedor_contacto_gestor_carga_by,
)
from .punto_venta import (  # noqa
    create_punto_venta,
    delete_punto_venta,
    edit_punto_venta,
    get_punto_venta_by,
    get_punto_venta_by_id,
    get_punto_venta_list,
)
from .punto_venta_contacto_gestor_carga import (  # noqa
    create_punto_venta_contacto_gestor_carga,
    delete_punto_venta_contacto_gestor_carga,
    edit_punto_venta_contacto_gestor_carga,
    get_punto_venta_contacto_gestor_carga_by,
)
from .remitente import (  # noqa
    create_remitente,
    delete_remitente,
    edit_remitente,
    get_remitente_by,
    get_remitente_by_id,
    get_remitente_list,
)
from .remitente_contacto_gestor_carga import (  # noqa
    create_remitente_contacto_gestor_carga,
    delete_remitente_contacto_gestor_carga,
    edit_remitente_contacto_gestor_carga,
    get_remitente_contacto_gestor_carga_by,
)
from .rol import get_rol_by_codigo, get_rol_list  # noqa
from .tipo_documento import (  # noqa
    get_tipo_documento_by_descripcion,
    get_tipo_documento_list,
)
from .user import create, get, get_by_email, get_by_username  # noqa
